# coding: utf-8

#
# This file is part of the IKPdb Debugger
# Copyright (c) 2016 by Cyril MORISSE, Audaxis
# Licence: MIT. See LICENCE at repository root
#
import sys
import os
import time
import threading
import ikp3db

TEST_MULTI_THREADING = True
TEST_EXCEPTION_PROPAGATION = True
TEST_POSTMORTEM = True
TEST_SYS_EXIT = 0
TEST_STEPPING = False
TEST_SUSPEND = True

# Note that ikp3db.set_trace() will reset/mess breakpoints set using GUI
TEST_SET_TRACE = False  

TCB = TEST_CONDITIONAL_BREAKPOINT = True

class Worker(object):
    def __init__(self):
        self._running = True
    
    def terminate(self):
        self._running = False
        
    def run(self, n):
        work_count = n
        while self._running and n > 0:
            print("Worker: Doing iteration: %s" % (work_count - n))
            if n == 2:
                print("break here")
                ikp3db.set_trace()
            n -= 1
            time.sleep(2)

ga = 5
gb ="coucou"
g_dict = {"Genesis": 1, "Don't Look Back": 2, 'array': [1,3,{'coucou': 3.14}]}
a_tuple = (1,'e', 3.14, ['a', 'b'])

class BigBear:
    color = "white"
    def __init__(self, name='unknown'):
        self._name = name
        
    def grumble(self):
        print("Roaaarrrrrrr")

def sub_function():
    return True

def the_function(p_nb_seconds):
    a_var = 18.3
    the_function_local_list = [1, 2, 3, 'cyril']
    a_beast = BigBear()
    print("ga=%s" % ga)
    
    print("Hello World")
    print("Ceci est la ligne avec le point d'arret")
    for loop_idx in range(p_nb_seconds):
        print("hello @ %s seconds" % loop_idx)
        time.sleep(1)
        if loop_idx == 6:
            if TEST_SET_TRACE:
                ikp3db.set_trace()  # will break on next line
            pass # Need this for set_trace()
            a_var = 98.3
            sub_function()                


def sub_raiser():
    raise Exception("IKPdb demo Exception")


def raiser():
    try:
        sub_raiser()
    except Exception as e:
        try:
            ikp3db.post_mortem(exc_info=sys.exc_info())
            print("Resuming execution after sending exception to debugger")
        except:
            print("IKPdb port_mortem() skipped since IKPdb is not available")

if __name__=='__main__':
    b = 0
    main_bear = BigBear("Cyril")
    print("Type of main_bear=%s" % type(main_bear))
    print("sys.argv=%s" % sys.argv)
    
    if TEST_SYS_EXIT:
        sys.exit(TEST_SYS_EXIT)
    
    if TEST_EXCEPTION_PROPAGATION:
        raiser()
    
    if TEST_MULTI_THREADING:
        w = Worker()
        t = threading.Thread(target=w.run, args=(5,))
        t.start()

    EXTRA_TIME = 0
    
    duration = 2 if TEST_STEPPING else 5 + EXTRA_TIME    
    the_function(duration)
    
    counter = 0
    if TEST_SUSPEND:
        print("Suspend test begin...")
        t0 = time.clock()
        while counter < 10000000:
            counter +=1
        t1 = time.clock()
        print("duration = %s" % (t1-t0))
        
        
    if TEST_MULTI_THREADING:
        w.terminate()
        t.join()
    
    
    if TEST_POSTMORTEM:
        print(5 / b)
    
    print("finished")