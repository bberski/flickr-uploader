#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

start_time = time.time()
tuples = []
x,y = (100000, 10)
for i in range(x):
    tuple_ = []
    for j in range(y):
        tuple_.append(random.randint(0, 9))
    tuples.append(tuple(tuple_))

print("--- %s data generated in %s seconds ---" % (x*y, time.time() - start_time))



def process_tuple(tuples):
    count_dict = {}
    for tuple_ in tuples:
        tuple_=tuple(sorted(tuple_))
        if tuple_ in count_dict:
            count_dict[tuple_] += 1
        else:
            count_dict[tuple_] = 1
    return count_dict

from multiprocessing import Pool

start_time = time.time()

## http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# cut tuples list into 5 chunks
tuples_groups = chunks(tuples, 5)
pool = Pool(5)
count_dict = {}
# processes chunks in parallel
results = pool.map(process_tuple, tuples_groups)
# collect results
for result in results:
    count_dict.update(result)

print("--- Multithread processed in %s seconds ---" % (time.time() - start_time))    



start_time = time.time()
count_dict = {}
for tuple_ in tuples:
    tuple_=tuple(sorted(tuple_))
    if tuple_ in count_dict:
        count_dict[tuple_] += 1
    else:
        count_dict[tuple_] = 1

print("--- Single thread processed in %s seconds ---" % (time.time() - start_time))
