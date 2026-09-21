import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
STORE = ROOT / "progress-store.js"


class ProgressStoreRuntimeTests(unittest.TestCase):
    def test_temporal_boundaries_are_classified_without_duplicate_contexts(self):
        script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(process.argv[1], 'utf8');
const window = {
  CustomEvent: class CustomEvent { constructor(name, init) { this.name = name; this.detail = init?.detail; } },
  dispatchEvent() {},
  localStorage: { getItem() { return null; }, setItem() {} }
};
const context = { window, CustomEvent: window.CustomEvent, navigator: {}, console, Date, setTimeout, clearTimeout };
vm.runInNewContext(source, context);
const classify = window.TrainingProgressStore.classifyTemporalRelation;
const base = new Date(2026, 8, 19, 12, 34, 0).getTime();
assert.strictEqual(classify(base, base + 30 * 1000), 'same-minute');
assert.strictEqual(classify(base, base + 2 * 60 * 1000), 'same-hour');
assert.strictEqual(classify(base, base + 2 * 60 * 60 * 1000), 'same-day');
assert.strictEqual(classify(base, base + 24 * 60 * 60 * 1000), 'other-day');
console.log(JSON.stringify({ ok: true }));
"""
        result = subprocess.run(
            ["node", "-e", script, str(STORE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(result.stdout), {"ok": True})

    def test_malformed_persisted_numbers_do_not_produce_nan_or_undefined_dashboard_values(self):
        script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(process.argv[1], 'utf8');
const fallback = JSON.stringify({
  progress: {
    day1: { routineId: 'day1', doneSeries: 'invalid', completedExercises: undefined, sessionEndedAt: 0, updatedAt: 'invalid' }
  },
  sessions: {
    'day1:bad': { sessionId: 'day1:bad', status: 'completed', completedSeries: 'invalid', updatedAt: 'invalid' }
  },
  activity: {
    bad: { activityKey: 'bad', routineId: 'day1', dayKey: '2026-09-19', completedSeries: 'invalid', updatedAt: 'invalid' }
  }
});
const window = {
  CustomEvent: class CustomEvent { constructor(name, init) { this.name = name; this.detail = init?.detail; } },
  dispatchEvent() {},
  localStorage: { getItem() { return fallback; }, setItem() {} }
};
const context = { window, CustomEvent: window.CustomEvent, navigator: {}, console, Date, setTimeout, clearTimeout };
vm.runInNewContext(source, context);
window.TrainingProgressStore.getDashboard().then((dashboard) => {
  assert.strictEqual(dashboard.recordedSeries, 0);
  assert.strictEqual(dashboard.todaySeries, 0);
  assert.strictEqual(dashboard.routines.length, 4);
  assert.strictEqual(dashboard.routines.find((routine) => routine.routineId === 'day4').totalSeries, 20);
  assert.ok(dashboard.routines.every((routine) => Number.isFinite(routine.doneSeries)));
  assert.ok(dashboard.routines.every((routine) => !Object.values(routine).includes(undefined)));
  console.log(JSON.stringify({ ok: true }));
}).catch((error) => { console.error(error); process.exit(1); });
"""
        result = subprocess.run(
            ["node", "-e", script, str(STORE)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True})

    def test_store_exposes_explicit_reset_operations(self):
        script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(process.argv[1], 'utf8');
const window = {
  CustomEvent: class CustomEvent { constructor(name, init) { this.name = name; this.detail = init?.detail; } },
  dispatchEvent() {},
  localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} }
};
const context = { window, CustomEvent: window.CustomEvent, navigator: {}, console, Date, setTimeout, clearTimeout };
vm.runInNewContext(source, context);
assert.strictEqual(typeof window.TrainingProgressStore.clearAll, 'function');
assert.strictEqual(typeof window.TrainingProgressStore.clearRoutine, 'function');
console.log(JSON.stringify({ ok: true }));
"""
        result = subprocess.run(
            ["node", "-e", script, str(STORE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(result.stdout), {"ok": True})

    def test_profile_is_saved_and_normalized_in_local_fallback(self):
        script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(process.argv[1], 'utf8');
let persisted = null;
const window = {
  CustomEvent: class CustomEvent { constructor(name, init) { this.name = name; this.detail = init?.detail; } },
  dispatchEvent() {},
  localStorage: {
    getItem() { return persisted; },
    setItem(_key, value) { persisted = value; },
    removeItem() {}
  }
};
const context = { window, CustomEvent: window.CustomEvent, localStorage: window.localStorage, navigator: {}, console, Date, setTimeout, clearTimeout };
vm.runInNewContext(source, context);
window.TrainingProgressStore.saveProfile({ displayName: 'Eva', birthDate: '1990-05-12', sex: 'female', heightCm: '171.5', goal: 'hypertrophy', units: 'metric' }).then(() => window.TrainingProgressStore.getProfile()).then((profile) => {
  assert.strictEqual(profile.profileId, 'local-default');
  assert.strictEqual(profile.displayName, 'Eva');
  assert.strictEqual(profile.birthDate, '1990-05-12');
  assert.strictEqual(profile.heightCm, 171.5);
  assert.strictEqual(profile.goal, 'hypertrophy');
  console.log(JSON.stringify({ ok: true }));
}).catch((error) => { console.error(error); process.exit(1); });
"""
        result = subprocess.run(
            ["node", "-e", script, str(STORE)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True})

    def test_backup_import_round_trip_preserves_profile_and_session_summary(self):
        script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(process.argv[1], 'utf8');
let persisted = null;
const window = {
  CustomEvent: class CustomEvent { constructor(name, init) { this.name = name; this.detail = init?.detail; } },
  dispatchEvent() {},
  localStorage: { getItem() { return persisted; }, setItem(_key, value) { persisted = value; }, removeItem() {} }
};
const context = { window, CustomEvent: window.CustomEvent, localStorage: window.localStorage, navigator: {}, console, Date, setTimeout, clearTimeout };
vm.runInNewContext(source, context);
const payload = {
  format: 'gymratik-backup', schemaVersion: 1,
  profile: { displayName: 'Respaldo', birthDate: '1988-01-02', sex: 'male', heightCm: 180, goal: 'strength', units: 'metric' },
  data: {
    progress: [{ routineId: 'day1', doneSeries: 3, totalSeries: 20, updatedAt: 10 }],
    sessions: [{ sessionId: 'day1:10', routineId: 'day1', label: 'Día 1', status: 'completed', completedSeries: 3, totalSeries: 20, updatedAt: 10 }],
    activity: [{ activityKey: 'day1:day1:10:2026-09-21T10:00', routineId: 'day1', completedSeries: 3, dayKey: '2026-09-21', updatedAt: 10 }]
  }
};
window.TrainingProgressStore.importData(payload).then(() => Promise.all([window.TrainingProgressStore.getProfile(), window.TrainingProgressStore.getHistory(), window.TrainingProgressStore.exportData()])).then(([profile, history, backup]) => {
  assert.strictEqual(profile.displayName, 'Respaldo');
  assert.strictEqual(history.length, 1);
  assert.strictEqual(history[0].completedSeries, 3);
  assert.strictEqual(backup.data.progress.length, 1);
  assert.strictEqual(backup.data.activity.length, 1);
  console.log(JSON.stringify({ ok: true }));
}).catch((error) => { console.error(error); process.exit(1); });
"""
        result = subprocess.run(
            ["node", "-e", script, str(STORE)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True})


if __name__ == "__main__":
    unittest.main()
