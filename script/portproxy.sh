#!/bin/bash
# Rok portproxy script
# Author: Max.Chiu

# linux
ncat --sh-exec "ncat 127.0.0.1 5555" -l 5555 --keep-open