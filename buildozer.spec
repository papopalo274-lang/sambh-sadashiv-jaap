[app]

# (str) Title of your application
title = Sambh Sadashiv Jaap

# (str) Package name
package.name = sambhsadashivjaap

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sambh.jaap

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf

# (str) Application version
version = 1.0.0

# (list) Application requirements
# Note: Kivy aur PyJNIus / Android dependencies included
requirements = python3,kivy==2.3.0,pyjnius,hostpython3,openssl

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Permissions needed for Android sound/vibration
android.permissions = INTERNET,VIBRATE

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a lib dir
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
