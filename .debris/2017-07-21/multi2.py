#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/codebasics/py/blob/master/Multiprocessing/multiprocessing_lock.py

import time
import multiprocessing


def Run(balance, lock):
    print(multiprocessing.current_process())
#    time.sleep(0.01)
    lock.acquire()
    balance.value = balance.value + 1
    print "i1", i
    lock.release()


def deposit(balance, lock):
    print(multiprocessing.current_process())
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        print "i1", i
        lock.release()

def withdraw(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value - 1
        print "i2", i
        lock.release()

if __name__ == '__main__':
    Lista = ["a", "b", "c", "d", "e", "f", "g", "h", "i" ,"j","a", "b", "c", "d", "e", "f", "g", "h", "i" ,"j",]
    Range = 5
    Process = 5
    balance = multiprocessing.Value('i', 1)
    manager = multiprocessing.Manager()
#    lock = manager.Lock()
    lock = multiprocessing.Lock()
    x = manager.list(Lista)
    pool = multiprocessing.Pool(processes=Process)
    for i in xrange(Range):
        print "i", i
        print "balance", balance.value
        pool.apply_async(func=Run, args=(balance , lock))
#        print "Z", Z
#        print "B", balance.value
#        if balance.value >= Max:
#            break
    pool.close()
    pool.join()

print(balance.value)


#Orginal
'''
import time
import multiprocessing

def deposit(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()

def withdraw(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()

if __name__ == '__main__':
    balance = multiprocessing.Value('i', 200)
    lock = multiprocessing.Lock()
    d = multiprocessing.Process(target=deposit, args=(balance,lock))
    w = multiprocessing.Process(target=withdraw, args=(balance,lock))
    d.start()
    w.start()
    d.join()
    w.join()
print(balance.value)
'''

