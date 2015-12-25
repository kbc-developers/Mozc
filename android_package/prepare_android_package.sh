#!/bin/sh

curr=`pwd`

cd ../src
./build_android_preinstall.sh

cd $curr
./copy_preinstall.sh

