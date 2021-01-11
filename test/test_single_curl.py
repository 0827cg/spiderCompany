#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 15:27
"""

import signal
import sys
from time import sleep

username = 'bubudee'
password = 'deebubu'

# def body(buf):
#     for item in buf.strip().split('\n'):
#         if item.strip():
#             print(item)
#
# def test(debug_type, debug_msg):
#     if len(debug_msg) < 300:
#         print("debug(%d): %s" % (debug_type, debug_msg.strip()))

def handle_ctrl_c(signal, frame):
    print("Got ctrl+c, going down!")
    sys.exit(0)
signal.signal(signal.SIGINT, handle_ctrl_c)

print("dd")

print("Who let the dogs out?:p")
sleep(10)

# conn.close()