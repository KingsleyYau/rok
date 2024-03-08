#!/bin/bash
# Run emulator script
# Author: Max.Chiu

../emulator/emulator -avd android30 -gpu off -no-window -noaudio -no-boot-anim -no-snapshot -http-proxy http://192.168.88.140:1080  
#./emulator/emulator -avd android34 -noaudio -no-boot-anim -gpu off -no-window