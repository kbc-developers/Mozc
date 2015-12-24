release_tools=../aosp/release_tools
zipalign=$release_tools/zipalign

input_apk=android/bin/MozcForAndroid-release-unsigned.apk
signed_apk=android/bin/MozcForAndroid-release-signed.apk
release_apk=android/bin/MozcForAndroid.apk

if [ -d out_android ]; then
  rm -R out_android
fi
if [ -f $signed_apk ]; then
  rm $signed_apk
fi
if [ -f $release_apk ]; then
  rm $release_apk
fi

if [ -f $release_apk ]; then
  rm $release_apk
fi

python build_mozc.py gyp --target_platform=Android --android_application_id=org.kbc_brick.mozc --android_hide_icon=1
python build_mozc.py build -c Release android/android.gyp:apk

if [ ! -f $input_apk ]; then
	exit 1
fi
java -jar $release_tools/signapk.jar $release_tools/platform.x509.pem $release_tools/platform.pk8 $input_apk $signed_apk
echo zipalign_process
$zipalign -v 4 $signed_apk $release_apk
