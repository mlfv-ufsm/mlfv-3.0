import rpyc
import pickle
import zlib as zl
import base64 as b64
import torch
import torchvision
from MLFV_Hosts import get_host
from MLFV_DB import decrease_runs
from chain import Chain


def send_function(con, obj):
    run = rpyc.utils.classic.teleport_function(con, obj.run)(obj)
    con.close
    return run


def exec_chain_function(c, p, ret, obj, pp, db):
    # print 'exec chain function params\nc: {}\np: {}\nret: {}\nobj: {}\npp: {}\ndb: {}\n'.format(c, p, ret, obj, pp, db)
    # print 'executed command: > {}'.format('cc=Chain({},{},{},{})'.format(str(c), p[c]['constraints'], p[c]['fn'], p[c]['params']))
    
    # import the object
    # exec("import " + obj.split('.')[0])
    # create the object with given parameters
    
    cc = Chain("'{}'".format(c), p[c]['constraints'], p[c]['fn'], p[c]['params'])

    h = get_host(cc, db)

    if h != None:
        # connect to the host
        con = rpyc.classic.connect(h[0], int(h[1]))
        # send the function to be executed there
        r = send_function(con, cc)

        if ret.find('set') != -1:
            # we need to compress the classifier
            # p[ret] = b64.b64encode(zl.compress(pickle.dumps(r), zl.Z_BEST_COMPRESSION))
            p[ret] = str(r.__dict__)
        else:
            p[ret] = r

        decrease_runs(db, h[0], h[1])

        return r
    else:
        return None

