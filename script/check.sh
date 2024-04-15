#!/bin/bash
# Author: Max.Chiu

IMAGE=`base64 -i 3.png`
echo ""
curl -v -X POST 'http://api.jfbym.com/api/YmServer/customApi' \
--header 'Content-Type: application/json' \
--data-raw "{\"token\":\"5K0Xgn0TczCwoNC8z8fEnc6OusYbxZBjGAl0DqUG_Aw\",\"type\":\"30009\",\"image\":\"$IMAGE\"}"