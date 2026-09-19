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
const context = { window, navigator: {}, console, Date, setTimeout, clearTimeout };
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


if __name__ == "__main__":
    unittest.main()
