#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
#import time

class Base(object):
    def __init__(self, id, lock):
        print(multiprocessing.current_process())
        self.id = id
#        self.Lista = Lista
        lock.acquire()
        balance.value = balance.value + 1
#        print "L", Lista[balance.value-1]
        print "bv", balance.value
#        self.Sleep()
        lock.release()

class Derived(Base):
    def __init__(self, id, lock):
        Base.__init__(self, id, lock)

#    def Run(self):
#        print "RR", self.id

def RunFunc(id, lock):
    print "Max2", Max
    if id >= Max:
#        print "HH",Lista[balance.value]
#        print "bv", balance.value
        return
    else:
        obj = Derived(id, lock)

#    return id
#    obj = Derived(id, lock)

def main(args):
    global Max
#    print "args", args
    Lista = args[0]
    Max = int(args[1])
    Process = int(args[2])
    Range = len(Lista)
    print "Lista", Lista
    print "Max1", Max
    print "Process", Process
    balance = multiprocessing.Value('i', 0)
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    x = manager.list(Lista)
    pool = multiprocessing.Pool(processes=Process)
    for i in xrange(Range):
        pool.apply_async(func=RunFunc, args=(i,lock))
#        print "B", balance.value
        if balance.value >= Max:
            break
    pool.close()
    pool.join()
    print "x", x
    print "SBV", balance.value
    print "L", x[0:balance.value ]

#def main(args):
    # parse arguments using optparse or argparse or what have you

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
