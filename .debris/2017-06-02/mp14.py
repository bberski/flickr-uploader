#!/usr/bin/env python
# -*- coding: utf-8 -*-


import multiprocessing
import time



class Base(object):
    def __init__(self, id, lock):
#        print(multiprocessing.current_process())
        self.Id = id
#        self.Lista = Lista
        lock.acquire()
        balance.value = balance.value + 1
#        print "L", Lista[balance.value-1]
        print "bv", balance.value
#        self.Sleep()
        lock.release()

#    def Run(self):
#        print "LKJLKJ"
#        pass

    def Sleep(self):
        print "SLEEP"
#        time.sleep(.2)

class Derived(Base):
    def __init__(self, id, lock):
        Base.__init__(self, id, lock)

#    def Run(self):
#        print "RR", self.Id

def RunFunc(id, lock):
    if id >= Max:
#        print "HH",Lista[balance.value]
#        print "bv", balance.value
        return
    else:
        obj = Derived(id, lock)
#        obj.Run()



if __name__ == "__main__":
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
        pool.apply_async(func=RunFunc, args=(i,lock))
        if balance.value >= Max:
            break
    pool.close()
    pool.join()
    print "x", x
    print "SBV", balance.value
    print "L", x[0:balance.value ]
