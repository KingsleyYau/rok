#!/bin/bash
# Run emulator script
# Author: Max.Chiu

./emulator/emulator -avd android30 -noaudio -no-boot-anim -gpu off -no-window -http-proxy http://192.168.88.140:1080 -verbose
#./emulator/emulator -avd android34 -noaudio -no-boot-anim -gpu off -no-window