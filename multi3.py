#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/codebasics/py/blob/master/Multiprocessing/multiprocessing_lock.py

import multiprocessing


def Run(balance, lock, findtext, x, Lista):
    print(multiprocessing.current_process())
    lock.acquire()
#    if findtext == Lista[balance.value]:
    if findtext in x:
        x = x.remove(findtext)
    else:
        x = Lista[balance.value : ]
        x.remove(findtext)
        print "xxx", x
    balance.value = balance.value + 1
    print "Lista", Lista
    lock.release()

    print "x", x
#    print "i1", balance.value
#    return balance.value

def main(Lista, Max, Process, findtext):
    Range = len(Lista)
    print "type", type(Lista)
    balance = multiprocessing.Value('i', 0)
    manager = multiprocessing.Manager()
    x = manager.list(Lista)
    lock = multiprocessing.Lock()
    groups = [0]*Range
    for i in xrange(Range):
        groups[i] = multiprocessing.Process(target=Run, args=(balance, lock, findtext, x, Lista))
        groups[i].start()
        groups[i].join()
        print "Value", balance.value
        if balance.value >= Max:
            break
    print "Finish", balance.value
    print "Lista", x[balance.value:]
