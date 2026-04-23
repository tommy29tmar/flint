from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

RUN_PATH = Path(__file__).resolve().parents[1] / "benchmarks" / "run.py"


def _load_run_module():
    spec = importlib.util.spec_from_file_location("benchmarks_run", RUN_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


run = _load_run_module()


class PromptLoadingTests(unittest.TestCase):
    def test_expansive_blocks_map_to_expected_ids(self) -> None:
        prompts = dict(run.load_expansive_en())

        self.assertEqual(set(prompts), {
            "smart-drafts-release-note",
            "outage-apology-email",
        })
        self.assertIn("Smart Drafts", prompts["smart-drafts-release-note"])
        self.assertIn("4-hour outage", prompts["outage-apology-email"])
        self.assertNotEqual(prompts["smart-drafts-release-note"], '"')

    def test_long_blocks_do_not_shift_when_header_mentions_separator(self) -> None:
        prompts = dict(run.load_long_en())

        self.assertIn("[capsule micro review]", prompts["rate-limit-xff-review"])
        self.assertIn(
            "POST /v1/orgs/:org_id/transfer",
            prompts["transfer-handler-review"],
        )
        self.assertIn(
            "POST /v1/media/upload-meta",
            prompts["body-size-rollout-plan"],
        )
        self.assertIn("512KB", prompts["body-size-rollout-plan"])
        self.assertNotIn('\n[Task]\n"', prompts["rate-limit-xff-review"])


if __name__ == "__main__":
    unittest.main()
