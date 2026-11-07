# PE-Reborn mondrian does not support FM broadcasting. Keep this legacy
# source available to other devices, but fail closed for mondrian even when
# an inherited board configuration accidentally enables BOARD_HAVE_QCOM_FM.
ifneq ($(TARGET_DEVICE),mondrian)
ifeq ($(BOARD_HAVE_QCOM_FM),true)
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := \
    FmIoctlsInterface.cpp \
    ConfigFmThs.cpp \
    FmPerformanceParams.cpp \
    ConfFileParser.cpp \
    FmRadioController.cpp \
    LibfmJni.cpp

LOCAL_C_INCLUDES := $(JNI_H_INCLUDE) \
    frameworks/base/core/jni/include \
    frameworks/base/include/media

LOCAL_SHARED_LIBRARIES := \
    libcutils \
    libdl \
    liblog \
    libmedia \
    libnativehelper \

ifeq ($(TARGET_QCOM_NO_FM_FIRMWARE),true)
    LOCAL_CFLAGS += -DQCOM_NO_FM_FIRMWARE
endif

LOCAL_MODULE := libfmjni
include $(BUILD_SHARED_LIBRARY)
endif # BOARD_HAVE_QCOM_FM
endif # TARGET_DEVICE != mondrian
