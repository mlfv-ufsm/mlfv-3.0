import multiprocessing
from MLFV_Manager import exec_chain_function


def parse_chain(c, p, db):
    p = multiprocessing.Manager().dict(p) #transform p in a multiprocessing dictionary

    if isinstance(c,tuple):
        return parse_seq(c,p,db)
    elif isinstance(c,list):
        return parse_par(c,p,db)
    else:
        print("Bug parsing the chain: "+ str(c))
        return None


def parse_seq(c, p, db):
    if isinstance(c,tuple) and len(c) > 1: # a sequential chain with more than one function
        for i in c:
            parse_seq(i,p,db)
    elif isinstance(c,list): # a parallel chain with more than one function
        parse_par(c,p,db)
    else:
        ret, obj, pp = parse_chain_obj(c) # single function, execute it
        return exec_chain_function(c, p, ret, obj, pp, db)


def parse_par(c, p, db):
    jobs=[]
    if isinstance(c,list) and len(c) > 1: # a parallel chain with more than one function
        for i in c:
            proc = multiprocessing.Process(target=parse_par,args=(i,p,db))
            jobs.append(proc)
            proc.start()
        for j in jobs:
            j.join() # waiting jobs
    elif isinstance(c,tuple): # a sequential chain with more than one function
        parse_seq(c,p,db)
    else: 
        ret, obj, pp = parse_chain_obj(c) # single function, execute it
        return exec_chain_function(c, p, ret, obj, pp, db)


def parse_chain_obj(c):
    # receives a string with the return, object, and parameters, parses it and returns the return variable, the object, and the list with parameters
    if not isinstance(c,str): # is a unary list
        c = c[0]
    c=c.replace(' ','')
    ret,f=c.split('=')
    obj,par=f.split('(')
    par=par.split(')')[0]
    pp = append_dic_par(par)
    return ret, obj, pp

def append_dic_par(pars):
    # parse the parameters to a list
    pp = pars.split(',')
    ret = '['
    for i in pp:
        ret+='p[\''+i+'\'],'
    ret = ret[:len(ret)-1]+']'
    return ret
