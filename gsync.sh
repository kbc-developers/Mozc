#!/bin/sh

if [ ! -f .gclient ]; then
  gclient config https://github.com/kbc-developers/android_packages_inputmethods_Mozc.git --name=. --deps-file=src/DEPS
fi

gclient sync
