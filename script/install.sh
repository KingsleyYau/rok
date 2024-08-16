#!/bin/bash
# Run emulator script
# Author: Max.Chiu

sdkmanager --list
sdkmanager "platforms;android-30" --no_https --proxy=http --proxy_host=192.168.88.133 --proxy_port=7778
sdkmanager "system-images;android-30;google_apis;x86_64" --no_https --proxy=http --proxy_host=192.168.88.138 --proxy_port=7778
sdkmanager "emulator" --no_https --proxy=http --proxy_host=192.168.88.138 --proxy_port=7778
avdmanager delete avd -n android30
avdmanager create avd -n android30 -k "system-images;android-30;google_apis;x86_64" 