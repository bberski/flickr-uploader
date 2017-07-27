#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import multiprocessing
#import time



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

def RunFunc(id, lock, Max):
    if id >= Max:
#        print "HH",Lista[balance.value]
#        print "bv", balance.value
        return
    else:
#        obj = Derived(id, lock)
        obj = Base(id, lock)
#        obj.Run()
    return id
