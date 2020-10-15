import rpyc
import pickle
import zlib as zl
import base64 as b64
from MLFV_Hosts import get_host
from MLFV_DB import decrease_runs


def send_function(con, obj):
    run = rpyc.utils.classic.teleport_function(con, obj.run)(obj)
    con.close
    return run


def exec_chain_function(c, p, ret, obj, pp, db):
    exec("import " + obj.split('.')[0])  # import the object
    exec('cc=' + obj + '(' + pp + ')')  # create the object with given parameters

    h = get_host(cc, db)

    if h != None:
        con = rpyc.classic.connect(h[0], int(h[1])) # connect to the host
        r=send_function(con, cc) # send the function to be executed there

        if ret == "cla":
            p[ret]=b64.b64encode(zl.compress(pickle.dumps(r), zl.Z_BEST_COMPRESSION)) # we need to compress the classifier
        else: 
            p[ret]=r

        decrease_runs(db, h[0], h[1])
 
        return r
    else:
        return None

