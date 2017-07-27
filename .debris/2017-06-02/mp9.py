#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import time

def Counter(i, event):
    i.value=1
    while i.value > 0 and not event.is_set():
        print("i: ",i.value)
        i.value += 1

def ValueTester(i, stopval, event):
    while True:
        if i.value >= stopval:
            event.set()
            break
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    stopval = 10.0
    num = mp.Value('d', 0.0)
    event = mp.Event()    
    counter = mp.Process(target=Counter, args=(num, event))
    counter.start()
    tester = mp.Process(target=ValueTester, args=(num, 10, event))
    tester.start()
    tester.join()
    counter.join()
    print("Process Complete")
    
