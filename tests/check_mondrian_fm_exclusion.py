#!/usr/bin/env python3
"""Host-only GNU Make regression checks for the mondrian FM JNI exclusion.

The Android 17 PE-Reborn product must not build libfmjni on mondrian even
when an inherited board setting accidentally enables BOARD_HAVE_QCOM_FM.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FmJniMondrianBuildGuardTest(unittest.TestCase):
    def evaluate_module(self, device: str, fm_flag: str) -> str:
        with tempfile.TemporaryDirectory(prefix="pe-fm-jni-test-") as folder:
            base = Path(folder)
            marker = base / "marker.mk"
            harness = base / "harness.mk"
            marker.write_text("$(info PE_FM_JNI_MODULE=$(LOCAL_MODULE))\n",
                              encoding="utf-8")
            harness.write_text(".PHONY: all\nall:\n\t@:\n",
                               encoding="utf-8")
            args = [
                "make", "--no-print-directory",
                "-f", str(ROOT / "Android.mk"),
                "-f", str(harness), "all",
                f"TARGET_DEVICE={device}",
                f"BOARD_HAVE_QCOM_FM={fm_flag}",
                "CLEAR_VARS=/dev/null",
                f"BUILD_SHARED_LIBRARY={marker}",
            ]
            result = subprocess.run(
                args, cwd=ROOT, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

    def test_mondrian_never_builds_fm_jni(self):
        for flag in ("true", "false", ""):
            with self.subTest(fm=flag):
                self.assertNotIn(
                    "PE_FM_JNI_MODULE=libfmjni",
                    self.evaluate_module("mondrian", flag),
                )

    def test_other_devices_keep_legacy_fm_opt_in(self):
        self.assertIn(
            "PE_FM_JNI_MODULE=libfmjni",
            self.evaluate_module("reference_other_device", "true"),
        )
        self.assertNotIn(
            "PE_FM_JNI_MODULE=libfmjni",
            self.evaluate_module("reference_other_device", "false"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
