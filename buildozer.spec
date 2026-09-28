[app]

# Application title
title = Naam Jaap

# Android package name
package.name = naamjaap

# Use your own reverse-domain identifier if you have one
package.domain = org.naamjaap

# main.py is in the repository root
source.dir = .

# Files that should be included in the APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3,json,ttf,otf

# Don't package build/cache directories
source.exclude_dirs = tests,bin,venv,.venv,.buildozer,.git,__pycache__

# Don't package these files
source.exclude_exts = spec,log,db

# Application version
version = 2.0.0

# Python + Kivy
requirements = python3==3.11.6,kivy==2.3.0

# Screen orientation
orientation = portrait

# Do not run fullscreen
fullscreen = 0


# ---------------------------------------------------------
# Android
# ---------------------------------------------------------

# Android API
android.api = 35

# Minimum Android API
android.minapi = 24

# NDK
android.ndk = 28c

# NDK API should match minimum API
android.ndk_api = 24

# Build modern 64-bit Android devices
android.archs = arm64-v8a

# Automatically accept Android SDK licenses in CI
android.accept_sdk_license = True

# Keep application data private
android.private_storage = True

# APK output
android.debug_artifact = apk
android.release_artifact = aab

# AndroidX
android.enable_androidx = True

# Backup
android.allow_backup = True


# ---------------------------------------------------------
# Permissions
# ---------------------------------------------------------

# This app uses local SQLite storage and does not need
# external storage permissions.
#
# Add INTERNET only if online functionality is later added.
# android.permissions = android.permission.INTERNET


# ---------------------------------------------------------
# Python-for-Android
# ---------------------------------------------------------

p4a.bootstrap = sdl2

# Use stable python-for-android master
p4a.branch = master


# ---------------------------------------------------------
# iOS / macOS
# ---------------------------------------------------------

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
