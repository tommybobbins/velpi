#!/bin/bash
/usr/local/bin/one_button.py 8
sleep 30
# Keep the time
/usr/local/bin/one_button.py 1
# Locate
/usr/local/bin/one_button.py 3
# Down to window 3
/usr/local/bin/one_button.py 4
/usr/local/bin/one_button.py 4
# Select
/usr/local/bin/one_button.py 1
# Buttons 5 and 7 will now open and close the windows
/usr/bin/redis-cli -h 433host set "velux/3" "Closed"
