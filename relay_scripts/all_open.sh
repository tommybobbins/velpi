#!/bin/bash
echo "All open" >/tmp/fullopen.txt
/usr/local/bin/one_button.py 3
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 1
sleep 1
/usr/local/bin/one_button.py 5
sleep 10
/usr/local/bin/one_button.py 3
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 1
/usr/bin/redis-cli -h 433host expire "velux/3" 14400
/usr/bin/redis-cli -h 433host set "velux/3" "Open"
/usr/bin/redis-cli -h 433host set "velux/2" "Open"
/usr/bin/redis-cli -h 433host set "velux/1" "Open"
