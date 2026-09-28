[app]

# Application metadata
title = Sambh Sadashiv Jaap
package.name = sambhsadashivjaap
package.domain = com.papopalo274.sambhsadashivjaap

# Source files and extensions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf

# Versioning
version = 1.0.0

# Dependencies
requirements = python3,kivy

# UI Settings
orientation = portrait
fullscreen = 0

# Android SDK / NDK Specifications
android.api = 33
android.minapi = 21
# Pin NDK to 25b to maintain compatibility with python-for-android
android.ndk = 25b
android.accept_sdk_license = True

# Target single architecture for cleaner and faster builds
android.archs = arm64-v8a

# Log level (2 = debug output)
log_level = 2
