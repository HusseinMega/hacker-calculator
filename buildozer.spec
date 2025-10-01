[app]
# (string) Title of your application
title = Hacker Calculator

# (string) Package name
package.name = hackercalc

# (string) Package domain (needed for Android/iOS)
package.domain = org.test

# (string) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include all relevant files)
source.include_exts = py,kv,png,jpg,gif,ttf

# (string) Application versioning
version = 1.0

# (list) Kivy requirements
requirements = python3,kivy

# (string) Presplash background color (for the loading screen)
presplash.background_color = #000000

# (string) Presplash animation (can be a gif)
# presplash.filename = %(source.dir)s/background.gif

# (string) App icon
# icon.filename = %(source.dir)s/icon.png

# (string) Supported orientation (portrait | landscape)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

[buildozer]
# (int) Log level (0 = error, 1 = info, 2 = debug (very verbose))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
