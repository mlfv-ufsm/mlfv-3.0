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
    #training parameters
    p['ds_train'] = np.asarray(pd.read_csv("./treino.csv"))
    p['classifier'] = 'RF'
    p['cla_opts'] = 20

    #selection parameters
    p['dataset'] = np.asarray(pd.read_csv(ds).dropna()) 
    p['columns'] = np.array([1, 2, 3, 6]) #'qT','fS','u2','u0'
    p['class_name'] = 11 #identifies the columns with the labels

    #preprocessing parameters
    p['scaler']='Standard'

    #generating the functions 
    s0 = "cla = training.Training(ds_train,classifier,cla_opts)"
    s1 = "selected = selection.Selection(dataset, columns, class_name)"
    s2 = "preproc = preprocessing.Preprocessing(selected, scaler)"
    s3 = "pred = testing.Testing(preproc,cla)"

    #composing and returning the chain
    c=([s0,(s1,s2)],s3)
    return c, p


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

