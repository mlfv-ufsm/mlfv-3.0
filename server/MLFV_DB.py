import sys
import multiprocessing


def insert_reg(db, r):
    if (len(r) < 6):
        print("Bad insertion")
        return False
    db[r['ip'], r['port']] = {
        'libs': r['libs'],
        'cpu': r['cpu'],
        'mem': r['mem'],
        'net': r['net'],
        'gpu': r['gpu'],
        'runs': 0
    }


def create_db():
    manager = multiprocessing.Manager()
    db = manager.dict()   
    return db


def remove_reg(db, r):
    del db[r['ip'], r['port']]
    return False


def decrease_runs(db, h, p):
    runs = db[h, p]['runs'] - 1
    r =  db[h, p]
    db[h, p]={
        'libs': r['libs'],
        'cpu': r['cpu'],
        'mem': r['mem'],
        'net': r['net'],
        'gpu': r['gpu'],
        'runs': runs
    } 


def get_less_busy(db, hl):
    less_runs = sys.maxsize
    for h in hl:
        rec = db[h] # Find the db register for each host in list hl
        if (rec['runs'] < less_runs):
            r = rec
            new_host = (h[0], h[1])
            less_runs = rec['runs']
    less_runs+=1 # update counter
    db[new_host]={
        'libs': r['libs'],
        'cpu': r['cpu'],
        'mem': r['mem'],
        'net': r['net'],
        'gpu': r['gpu'],
        'runs': less_runs
    } 
    return new_host


def get_hosts_cpu_mem_gpu(db, cpu, mem, gpu):
    ret = []
    for h in db.keys():
        # filter cpu and memory constraints
        if int(db[h]['mem']) >= int(mem):
            if gpu and db[h]['gpu']['is_enabled']:
                ret.append((
                    h[0],
                    h[1],
                    db[h]['libs'],
                    db[h]['cpu'],
                    db[h]['mem'],
                    db[h]['net'],
                    db[h]['gpu'],
                    db[h]['runs']
                ))
            elif int(db[h]['cpu']) >= int(cpu):
                ret.append((
                    h[0],
                    h[1],
                    db[h]['libs'],
                    db[h]['cpu'],
                    db[h]['mem'],
                    db[h]['net'],
                    db[h]['gpu'],
                    db[h]['runs']
                ))
    if ret == []:
        print("Error: no compatible host found (mem or cpu constraints)!")
    return ret


