[app]

# (str) Title of your application
title = Sambh Sadashiv Jaap

# (str) Package name
package.name = sambhsadashivjaap

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sambh.jaap

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf

# (str) Application version
version = 1.0.0

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Application requirements
requirements = python3,kivy==2.3.0,pyjnius,hostpython3,openssl

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Permissions needed
android.permissions = INTERNET,VIBRATE

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a lib dir
android.copy_libs = 1

# (str) Target architectures
android.archs = arm64-v8a, armeabi-v7a

# (str) Explicitly specify Python version for p4a
p4a.python_version = 3.11

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
