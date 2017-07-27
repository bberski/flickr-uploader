#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
from threading import Thread
import threading
import time

lock = threading.Lock()

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
        
        
def exp1_thread(counter):
    with lock:
        time.sleep(.3)
        print counter[0]
        counter[0] = counter[0] + 1

def test():
    # 1) Init a Thread pool with the desired number of threads
    pool = ThreadPool(10)
    counter = [0]
    for i in range(0, 20):
        pool.add_task(exp1_thread, counter)

#    pool.close() #we are not adding any more processes
#    pool.join() #tell it to wait until all threads are done before going on

    # 3) Wait for completion
    pool.wait_completion()
    print "type", type(int(counter[0]))
    print "counter", int(counter[0])
if __name__ == "__main__":
    test()
