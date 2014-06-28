#!/bin/bash
/usr/bin/redis-cli -h 433host set "velux/3" "Half"
/usr/bin/redis-cli -h 433host set "velux/2" "Half"
/usr/bin/redis-cli -h 433host set "velux/1" "Half"
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
sleep 12
/usr/local/bin/one_button.py 6
sleep 1
/usr/local/bin/one_button.py 3
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 4
sleep 1
/usr/local/bin/one_button.py 1
/usr/bin/redis-cli -h 433host expire "velux/3" 14400
