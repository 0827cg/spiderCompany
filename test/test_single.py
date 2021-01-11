#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 15:25
"""

import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()