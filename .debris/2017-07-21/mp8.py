#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Value, Lock
import multiprocessing
import time



class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1
            print "V", self.val.value

    def value(self):
        with self.lock:
            return self.val.value

def func(counter):
    for i in range(50):
        time.sleep(0.01)
        counter.increment()


class MyProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            pass
        print "You exited!"

    def shutdown(self):
        print "Shutdown initiated"
        self.exit.set()


if __name__ == "__main__":


    counter = Counter(0)
    pool_size = 10
    pool = MyProcess()
    print "M", pool

    for x in range(pool_size):
        p.start()

#        pool.append(Process(target=func, args=(counter,)))

#    for p in pool:
#        p.start()
    print "Waiting for a while"
    time.sleep(3)
#    pool.shutdown()
    time.sleep(3)
    print "Child process state: %d" % process.is_alive()
    
