from MLFV_DB import get_less_busy, get_hosts_cpu_mem

openstack=False

def get_less_busy_host(hr, db):
    lb = None
    while lb == None:
        lb = get_less_busy(db, hr)
    return (lb[0],lb[1])


def get_host(c, db):
    hr = get_compatible_hosts(c, db)
    if len(hr) == 0:
        print("Bug: no compatible host found!")
        return None
    h = get_less_busy_host(hr, db)
    print("  Sending \'"+str(c.name)+"\' to: "+str(h[0])+"("+str(h[1])+")")
    return h


def get_compatible_hosts(c, db):
    hs = []
    hr = []

    # filter cpu and memory constraits using the provided values
    hosts = get_hosts_cpu_mem(db, c.constr.cpu, c.constr.mem)

    if openstack: # get values from openstack gnocchi plugin
        for i in hosts: # filters again cpu and memory using 'online' values
            (cpu, memory, bandwidth) = get_host_info(i[0], 'eth0') 
            if cpu < c.constr.cpu or memory < c.constr.mem or bandwidth < c.constr.net:
                x.remove(i) #

    else: # openstack not available, using the provided parameters for network
        # filter network constraints 
        for i in hosts:
            #TODO: Openstack & Ceilometer integration
            if (int(i[5]) >= int(c.constr.net)):
                hs.append((i[0],i[1],sorted(i[2].split(',')))) # append (host,port)
    l = sorted(c.constr.imports.split(','))
    
    # library constraints
    for h,p,libs in hs:
        if len(set(l).intersection(libs)) == len(l):
            hr.append((h,p))

    return hr

