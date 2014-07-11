#!/bin/bash
/usr/bin/redis-cli -h 433host set "velux/3" "Open"
echo "Full open" >/tmp/fullopen.txt
/usr/local/bin/one_button.py 5
/usr/bin/redis-cli -h 433host expire "velux/3" 14400
