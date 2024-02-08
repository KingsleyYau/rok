#!/bin/bash
# Run emulator script
# Author: Max.Chiu

adb shell am force-stop com.lilithgames.rok.offical.cn
adb shell am start -n com.lilithgames.rok.offical.cn/com.harry.engine.MainActivity