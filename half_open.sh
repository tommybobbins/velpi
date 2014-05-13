#!/bin/bash
echo "Half Opening" >/tmp/opening.txt
/usr/local/bin/one_button.py 7
sleep 40
/usr/local/bin/one_button.py 5
sleep 12
/usr/local/bin/one_button.py 6
date >>/tmp/opening.txt
