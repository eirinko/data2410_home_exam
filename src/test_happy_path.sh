#!/bin/bash
set -xe

# clean up result.jpg from last run
rm -f result.jpg

# kill any process if it is still running
# pkill -e "python3 application.py" && true
killall python3

# run server in background 
python3 application.py -s &
sleep 1

# run client and wait for it to finish
python3 application.py -c -f iceland_safiqul.jpg

if diff result.jpg iceland_safiqul.jpg; then
    echo "SUCCESS"
else
    echo "FAILURE"
fi
