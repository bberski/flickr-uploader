#!/usr/bin/env python
# -*- coding: utf-8 -*-


from multiprocessing import Process, Queue, cpu_count
import random
import time

TIMEOUT = 5


class Pool(object):
    """Very basic process pool with timeout."""

    def __init__(self, size=None, timeout=15):
        """Create new `Pool` of `size` concurrent processes.

        Args:
            size (int): Number of concurrent processes. Defaults to
                no. of processors.
            timeout (int, optional): Number of seconds to wait before
                killing the process.
        """
        self.size = size or cpu_count()
        self.timeout = timeout
        self.pool = []
        self._counter = 1
        self._q = Queue()

    def map(self, func, it):
        """Call `func` with each element in iterator `it`.

        Args:
            func (callable): Function/method to call.
            it (iterable): List of arguments to pass to each call of `func`.

        Returns:
            list: The results of all the calls to `func`.
        """
        while True:
            if len(it) and len(self.pool) < self.size:
                arg = it.pop(0)
                self._start_process(func, (arg,))
                continue

            if len(self.pool) == len(it) == 0:  # Finished
                break

            pool = []
            for proc in self.pool:
                if not proc.is_alive():
                    print('{} done.'.format(proc.name))
                    continue

                age = time.time() - proc.start_time
                if age >= self.timeout:
                    print('{} killed.'.format(proc.name))
                    proc.terminate()
                    continue

                pool.append(proc)

            self.pool = pool
            time.sleep(0.01)

        results = []
        while not self._q.empty():
            results.append(self._q.get())

        return results

    def _start_process(self, target, args):
        """Call `target` with `args` in a separate process.

        The result of the call is returned via `self._q`.

        Args:
            target (callable): Function to call in new process.
            args (it): Tuple/list of arguments to pass to `target`.

        """

        def _wrapper():
            """Closure around the callable."""
            result = target(*args)
            self._q.put(result)

        proc = Process(target=_wrapper,
                       name='Process#{}'.format(self._counter))
        proc.start()
        print('{} started.'.format(proc.name))
        proc.start_time = time.time()
        self.pool.append(proc)
        self._counter += 1


def worker(key):
    """Demo function to call via `Pool`.

    Each call has a 1/3 chance of running for 1 second, running for
    more than 1 second but less than `TIMEOUT` and for longer than
    `TIMEOUT`, i.e. it will be killed by `Pool`.
    """
    # Some process which occassionally takes a long time
    coin = random.randint(0,2)
    if coin == 0:
        seconds = random.randint(TIMEOUT+1, 1000)
    elif coin == 1:
        seconds = random.randint(2, TIMEOUT)
    else:
        seconds = 1

    print('Process#{} will run for {} second(s).'.format(key, seconds))
    time.sleep(seconds)
    print('Process#{} ran for {} second(s).'.format(key, seconds))
    return seconds


if __name__ == '__main__':
    keys = range(1,20)
    p = Pool(20, TIMEOUT)
    results = p.map(worker, keys)
    print(results)
