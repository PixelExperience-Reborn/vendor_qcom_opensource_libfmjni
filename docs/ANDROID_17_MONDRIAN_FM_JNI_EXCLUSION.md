# Android 17 mondrian FM JNI build exclusion

Scope: PixelExperience-Reborn independent AOSP Android 17 for POCO F5 Pro / Redmi K60 (`mondrian`, SM8475).

## Source and product decision
Historical `vendor/qcom/opensource/libfmjni` PE `seventeen`: `e33227ed63c6b8e7df0b638f556bf14fa99acd83` (April 23, 2020), tree `49ae9c31f7ef85cb6b3e2a902cb45ca2c93d84c6`. The JNI shared library `libfmjni` is selected by `BOARD_HAVE_QCOM_FM=true` in `Android.mk` and uses historical native FM controller/IOCTL source. This is **FM broadcast radio**, not mobile radio / IMS / RIL / LTE.

The user does not want FM receiver features in the mondrian ROM. Keep source history for other devices only; do not add FM apps, privileged permissions, service, FM HCI, HAL, JNI or product makefile flags.

## Source-level exclusion
A new outer `ifneq ($(TARGET_DEVICE),mondrian)` encloses the original `BOARD_HAVE_QCOM_FM` gate. The legacy `libfmjni` module can therefore never be registered by this makefile on mondrian even if an inherited board config accidentally sets the FM flag. Other devices retain the prior opt-in behavior; historical JNI sources are untouched.

`tests/check_mondrian_fm_exclusion.py` evaluates the actual makefile with GNU Make using test stubs:
- `mondrian`: true/false/empty FM flag — never registers `libfmjni`.
- unrelated device: true registers `libfmjni`, false does not.

This is an independent defense-in-depth layer. The manifest already excludes both `vendor/qcom/opensource/libfmjni` and `vendor/qcom/opensource/fm-commonsys` by name/path; it also must reject accidental imports in all isolated candidates. The old `vendor/qcom/opensource/interfaces` tree contains FM HIDL and is likewise unsuitable as a wholesale checkout.

**Status:** makefile change and host-only regression. Not an Android17 build or proof of final installed-file list. Confirm no `libfmjni`, `qcom.fmradio`, FM HCI HAL or FM permissions in the final native PE-Reborn mondrian product artifact; do not confuse `libfmpal` in some historical audio lists with proof of actual FM hardware or remove its other users without ABI analysis.
