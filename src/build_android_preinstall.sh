#!/bin/sh

input_apk=android/bin/MozcForAndroid-release-unsigned.apk

if [ -d out_android ]; then
  rm -R out_android
fi

#python build_mozc.py gyp --target_platform=Android --android_application_id=org.kbc_brick.mozc --android_hide_icon=1
python build_mozc.py gyp --target_platform=Android --android_hide_icon=1
python build_mozc.py build -c Release android/android.gyp:apk

if [ ! -f $input_apk ]; then
	exit 1
fi
