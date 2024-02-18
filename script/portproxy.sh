#!/bin/bash
# Rok portproxy script
# Author: Max.Chiu

# linux
ncat -c "ncat 127.0.0.1 5555" -l 9999 --keep-open