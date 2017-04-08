#!/usr/bin/env python
print "forks child processes until you type 'q'"
import os
def child():
    print('Hello from child', os.getpid())
    os._exit(0) # else goes back to parent loop

def parent():
    newpid = os.fork()
    print(newpid)
    if newpid == 0:
        child()

parent()