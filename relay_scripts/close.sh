#!/bin/bash
echo "Close" >/tmp/close.txt
/usr/local/bin/one_button.py 7
echo "Finished" >>/tmp/close.txt
date >>/tmp/close.txt
