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


if __name__ == "__main__":
    unittest.main()
