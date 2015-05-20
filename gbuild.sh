#!/bin/sh

cd src

python build_mozc.py clean --target_platform=Android
python build_mozc.py gyp --target_platform=Android
python build_mozc.py build -c Release android/android.gyp:apk

cd ..

