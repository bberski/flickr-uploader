#!/usr/bin/env python
# -*- coding: utf-8 -*-


import multiprocessing
import time
#import multi
from multi import *



def RunFunc1(id, lock):
    if id >= Max:
#        print "HH",Lista[balance.value]
#        print "bv", balance.value
        return
    else:
#        obj = Derived(id, lock)
        obj = Base(id, lock)
#        obj.Run()
#    return balance


if __name__ == "__main__":
#    global balance
#    global Max
    Lista = ["a", "b", "c", "d", "e", "f", "g", "h", "i" ,"j","a", "b", "c", "d", "e", "f", "g", "h", "i" ,"j",]
    Max = 6
    Range = len(Lista)
    Process = 5
    balance = multiprocessing.Value('i', 0)
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    x = manager.list(Lista)
    pool = multiprocessing.Pool(processes=Process)
    for i in xrange(Range):
        async_result = pool.apply_async(func=RunFunc1, args=(i,lock, Max))
#        print "X", async_result.get()
        print "B", balance.value
        if balance.value >= Max:
            break
    pool.close()
    pool.join()
    print "x", x
    print "SBV", balance.value
    print "L", x[0:balance.value ]
