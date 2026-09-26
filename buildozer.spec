[app]

# App details
title = My Application
package.name = myapp
package.domain = org.test

# Source code location
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Application versioning
version = 0.1

# Application requirements (Apne packages yahan add karein)
requirements = python3,kivy

# Android Specific Settings
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_licenses = True

# Buildozer log level (2 = debug info)
log_level = 2

# Display settings
orientation = portrait
fullscreen = 0

[buildozer]

# Log level and warnings
log_level = 2
warn_on_root = 1
