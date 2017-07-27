#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

def myfunction(i, event):
    if not event.is_set():
        print i
    if i == maxnr:
#        event.put()
        event.set()

if __name__ == "__main__":
    pool_size = 20
    maxnr = 100 
    p= multiprocessing.Pool(pool_size) 
    m = multiprocessing.Manager()
#    event = m.Event()
    event = m.Event()
    for i in range(maxnr+maxnr):
        p.apply_async(myfunction , (i, event))
    p.close()

    event.wait()  # We'll block here until a worker calls `event.set()`
    p.terminate() # Terminate all processes in the Pool
    
#    print "nr", event.get()
