#!/bin/sh

#copy files
mozc_src_dir=../src
package_dir=./android_package/android_packages_inputmethods_Mozc

cp -f $mozc_src_dir/android/assets/* $package_dir/assets/
cp -f $mozc_src_dir/android/libs/*.jar $package_dir/libs/
cp -f $mozc_src_dir/android/libs/armeabi-v7a/libmozc.so $package_dir/jni/lib/libmozc.so
cp -f $mozc_src_dir/android/protobuf/bin/classes.jar $package_dir/libs/protobuf.jar

rm -rf $package_dir/res
cp -R $mozc_src_dir/out_android/Release/gen/android/resources/res $package_dir/

rm -f $package_dir/res/values/launcher_icon_preinstall_bools.xml
cp -f $mozc_src_dir/android/static_resources/launcher_icon_resources/launcher_icon_preinstall_bools.xml $package_dir/res/values/launcher_icon_preinstall_bools.xml

rm -rf $package_dir/src/com
cp -R $mozc_src_dir/android/src/com $package_dir/src/

rm -rf $package_dir/src/org
cp -R $mozc_src_dir/android/gen_for_adt/org $package_dir/src/

cp -f $mozc_src_dir/android/AndroidManifest.xml $package_dir/
cp -f $mozc_src_dir/android/ant.properties $package_dir/
cp -f $mozc_src_dir/android/build.xml $package_dir/
cp -f $mozc_src_dir/android/proguard-project.txt $package_dir/
#cp -f android/project.properties $package_dir/

cd $package_dir
./fix_resources_ns.sh
