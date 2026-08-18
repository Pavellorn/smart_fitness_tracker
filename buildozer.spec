[app]
title = Smart Fitness
package.name = smartfitness
package.domain = com.pavellorn
source.dir = .
source.include_exts = py,kv,json,png,jpg,atlas,ttf
source.exclude_dirs = tests, .git, .venv, __pycache__, build, bin
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.permissions = VIBRATE
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
