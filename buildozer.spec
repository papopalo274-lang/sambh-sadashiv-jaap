[app]

# (High Fix) App identity - update package.domain and package.name to match your real organization/app
title = Your App Name
package.name = your_app_name
package.domain = com.yourdomain

# Source files and inclusions
source.dir = .
# (Medium Fix) Restored wav, mp3, and ttf extensions to prevent missing media and custom font assets at runtime
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf

# (Minor Fix) Restored versioning back to 1.0.0
version = 1.0.0

# Application requirements
requirements = python3,kivy

# UI configuration
orientation = portrait
fullscreen = 0

# Android specific configurations
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
