# MLFV: Machine Learning Function Virtualization

MLFV was created using Python 2.7 ( and we did not update it yet ):


## Installing the necessary dependencies

### Server: 

```bash
pip install sklearn rpyc
```

### Client: 

```bash
pip install rpyc <and the libraries that are going to be provided in each client (e.g. sklearn, pandas)>
```


## Testing MLFV

First you need to start MLFV_Module:

```bash
python MLFV_Module.py
```


Then, you have to start, at least one client

python init_client.py <server> <port> <libraries_to_be_shared> <cpu_speed> <memory_capacity> <network_speed>

```bash
python init_client.py localhost 8889 "os,numpy,sys,timeit,pandas,sklearn.ensemble,sklearn.preprocessing,sklearn.metrics" 3000 8 100
```


Finally you can start testing:

python test_MLFV.py <filename_with_data_to_be_classified>

```bash
python test_MLFV.py 01mb.csv
```

## OpenStack and Gnocchi

For running with openstack and gnocchi, it is necessary to install the following libraries:

```bash
pip install keystoneauth1 gnocchiclient
```

It is also necessary to set openstack=True in MLFV_Hosts.py and configure OpenStack and Gnocchi parameters in MLFV_Gnocchi.py


