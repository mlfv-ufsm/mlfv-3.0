import sys
import rpyc
import timeit
import multiprocessing
import numpy as np
import pandas as pd
import tensorflow as tf

MLFV_SERVER_HOST="127.0.0.1"
MLFV_SERVER_PORT=15088

def get_chain():
    p = {}

    dataset = tf.keras.datasets.mnist.load_data()

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    p['model_json'] = model.to_json()
    p['dataset'] = dataset

    p['optimizer'] = 'adam'
    p['loss'] = 'sparse_categorical_crossentropy'
    p['metrics'] = ['accuracy']

    #generating the functions 
    s0 = "prep_data = preprocessing.Preprocessing(dataset)"
    s1 = "cla = training.Training(model_json, optimizer, loss, metrics, prep_data)"
    s2 = "pred = testing.Testing(cla, model_json, optimizer, loss, metrics, prep_data)"

    #composing and returning the chain
    return (s0, s1, s2), p


#connects to the MLFV Module and sends the chain (c) with their parameters (p)
def send_chain(c,p):
    start = timeit.default_timer()

    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
    rpyc.core.protocol.DEFAULT_CONFIG['sync_request_timeout'] = None
    
    con = rpyc.connect(MLFV_SERVER_HOST, MLFV_SERVER_PORT, config = rpyc.core.protocol.DEFAULT_CONFIG)

    ret = con.root.exec_chain(c,p)
    end = timeit.default_timer()
    time = end - start
    print("Total execution time: "+str(time))
    return ret


#executes a single chain
def single():
    c,p = get_chain()
    x = send_chain(c,p)


#perfoms multiple executions in parallel
def multiple(num_par):
    jobs = []
    c,p = get_chain()
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
    if len(sys.argv) == 1:
        single()
    else:
        multiple(int(sys.argv[1]))

