#!/bin/bash
/usr/bin/redis-cli -h 433host set "velux/3" "Half"
echo "Half Opening" >/tmp/opening.txt
/usr/local/bin/one_button.py 5
sleep 12
/usr/local/bin/one_button.py 6
date >>/tmp/opening.txt
/usr/bin/redis-cli -h 433host expire "velux/3" 3600 
