#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import multiprocessing

def deposit(balance, lock, maxnr, top, event):
    for i in range(maxnr):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()
        print(multiprocessing.current_process())
        print "b", balance.value
        if balance.value > top:
#            print "X", start_time
#            print time.clock() - start_time, "seconds"
            break


if __name__ == '__main__':
    global start_time
    start_time = time.clock()
    top = 1000
    pool_size = 5
    maxnr = 10000 
    p= multiprocessing.Pool(processes=10)
    balance = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    m = multiprocessing.Manager()
    event = m.Event()
#    w = multiprocessing.Process(target=withdraw, args=(balance,lock))
    for i in range(pool_size):
        d = p.Process(target=deposit, args=(balance,lock, maxnr, top, event))
        d.start()
#    pool.join()
    pool.close()
    print(balance.value)
    print "d", d
#    for i in range(pool_size):
#        d.join()
    print time.clock() - start_time, "seconds"

