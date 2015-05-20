#!/bin/sh

if [ ! -f .gclient ]; then
  gclient config https://github.com/kbc-developers/mozc.git --name=. --deps-file=src/DEPS
fi

gclient sync
