[app]

title = Sambh Sadashiv Jaap
package.name = sambhsadashivjaap
package.domain = org.sambh.jaap
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf
version = 1.0.0
icon.filename = %(source.dir)s/icon.png
requirements = python3==3.11.9,kivy==2.3.0,pyjnius,hostpython3,openssl
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET,VIBRATE
android.logcat_filters = *:S python:D
android.copy_libs = 1
android.archs = arm64-v8a, armeabi-v7a
p4a.python_version = 3.11

[buildozer]

log_level = 2
warn_on_root = 1
