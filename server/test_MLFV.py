import sys
import rpyc
import timeit
import multiprocessing
import numpy as np
import pandas as pd

MLFV_SERVER_HOST="127.0.0.1"
MLFV_SERVER_PORT=15088

def get_chain(ds):
    p = {}

    p['optimizer'] = 'adam'
    p['loss'] = 'sparse_categorical_crossentropy'
    p['metrics'] = ['accuracy']

    #generating the functions 
    s0 = "cla = training.Training(optimizer, loss, metrics)"
    s3 = "pred = testing.Testing(cla)"

    #composing and returning the chain
    return (s0, s3), p


#connects to the MLFV Module and sends the chain (c) with their parameters (p)
def send_chain(c,p):
    start = timeit.default_timer()

    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
    con = rpyc.connect(MLFV_SERVER_HOST, MLFV_SERVER_PORT, config = rpyc.core.protocol.DEFAULT_CONFIG)

    ret = con.root.exec_chain(c,p)
    end = timeit.default_timer()
    time = end - start
    print("Total execution time: "+str(time))
    return ret


#executes a single chain
def single(ds):
    c,p = get_chain(ds)
    x = send_chain(c,p)


#perfoms multiple executions in parallel
def multiple(ds,num_par):
    jobs = []
    c,p = get_chain(ds)
    for i in range(num_par):
        print("Sending "+str(i))
        proc = multiprocessing.Process(target=send_chain, args=(c, p))
        jobs.append(proc)
        proc.start()
    for j in jobs:
        print("Waiting for jobs")
        j.join()
        print(j.name+'exitcode = ' +str(j.exitcode))


if __name__ == "__main__":
    if (len(sys.argv) == 1 or len(sys.argv) > 3):
        print("For executing a single chain, use: "+sys.argv[0]+"<filename>")
        print("For executing multiple chains in parallel, use: "+sys.argv[0]+"<filename> <num_par>")
        print("  where\n    <filename> = csv file with to be classified\n    <num_par> = number of executions in parallel")
    elif len(sys.argv) == 2:
        single(sys.argv[1])
    else:
        multiple(sys.argv[1],int(sys.argv[2]))

