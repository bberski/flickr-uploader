#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import time

def myfunction(i, event, maxnr, balance):


    if not event.is_set():
#        print(multiprocessing.current_process())
#        lock.acquire()
        balance.value = i
#        lock.release()
        print balance.value
    if i == maxnr:
        event.set()

if __name__ == "__main__":
    start_time = time.clock()
    maxnr = 1000
    pool_size = 1
    p= multiprocessing.Pool(processes=pool_size) 
    m = multiprocessing.Manager()
    balance = m.Value('i', 0)
    lock = multiprocessing.Lock()
    event = m.Event()
    print "b", balance

    for i in range(maxnr+1):
        p.apply_async(myfunction , (i, event, maxnr, balance))

    p.close()

    event.wait()  # We'll block here until a worker calls `event.set()`
    p.terminate() # Terminate all processes in the Pool
    print "Value", balance.value
    print time.clock() - start_time, "seconds"
