#!/bin/bash
/usr/bin/redis-cli -h 433host set "velux/3" "Closed"
echo "Close" >/tmp/close.txt
/usr/local/bin/one_button.py 7
echo "Finished" >>/tmp/close.txt
date >>/tmp/close.txt
/usr/bin/redis-cli -h 433host expire "velux/3" 3600
