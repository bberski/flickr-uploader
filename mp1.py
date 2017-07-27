#!/usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing import Pool, Value
#from time import sleep
from collections import Counter
import sys

counter = None

def myexcepthook(exctype, value, traceback):
    for p in multiprocessing.active_children():
       p.terminate()

def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args

def analyze_data(args):
    print "ARG", args
    ''' increment the global counter, do something with the input '''
    global counter
    # += operation is not atomic, so we need to get a lock:
    with counter.get_lock():
        if counter.value < 5:
            counter.value += 1
            print "XX", counter.value
            return args * 1
        else:
            print "Close", inputs
            p.terminate()
            p.join()
#            p.close()
#            sys.excepthook = myexcepthook
            return

if __name__ == '__main__':
    #inputs = os.listdir(some_directory)

    #
    # initialize a cross-process counter and the input lists
    #
    counter = Value('i', 0)
    inputs = ["a", "b", "c", "d", "e", "f", "g", "h", "i" ,"j",]

    #
    # create the pool of workers, ensuring each one receives the counter 
    # as it starts. 
    #
    counts = Counter()
    p = Pool(processes=4)
    p = Pool(initializer = init, initargs = (counter, ))
#    p = Pool(initializer = init, initargs = (counter, Dict ))
    i = p.map_async(analyze_data, inputs, chunksize = 1)
#    i = p.map_async(analyze_data, inputs, chunksize = 2)
#    p.close()
    i.wait()
    print "c", counter.value
    print "H", i.get()
