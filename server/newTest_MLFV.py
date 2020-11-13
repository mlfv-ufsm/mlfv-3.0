import sys
import rpyc
import timeit
import multiprocessing
import numpy as np
import pandas as pd
import torchvision

MLFV_SERVER_HOST = "127.0.0.1"
MLFV_SERVER_PORT = 15088

def get_chain():
  p = {}
  
  transform = "'torchvision.transforms.Compose([torchvision.transforms.ToTensor(),torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])'"

  imports = 'os,sys,timeit,numpy,pandas,torch,torchvision'

  p['trainset'] = {}
  p['trainloader'] = {}
  p['testset'] = {}
  p['testloader'] = {}
  p['classes'] = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

  p['trainset']['constraints'] = {
    'imports': imports,
    'cpu': 2,
    'mem': 30000000,
    'net': 100,
  }
  p['trainset']['fn'] = 'torchvision.datasets.CIFAR10(root,train,download,transform)'
  p['trainset']['params'] = {
    'root': "'./data'",
    'train': True,
    'download': True,
    'transform': transform
  }

  p['trainloader']['constraints'] = {
    'imports': imports,
    'cpu': 2,
    'mem': 30000000,
    'net': 10,
  }
  p['trainloader']['fn'] = 'torch.utils.data.DataLoader(dataset,batch_size,shuffle,num_workers)'
  p['trainloader']['params'] = {
    'dataset': { 'type': 'key', 'target': "p['testset']" },
    'batch_size': 4,
    'shuffle': True,
    'num_workers': 2
  }

  p['testset']['constraints'] = {
    'imports': imports,
    'cpu': 2,
    'mem': 30000000,
    'net': 100,
  }
  p['testset']['fn'] = 'torchvision.datasets.CIFAR10(root,train,download,transform)'
  p['testset']['params'] = {
    'root': "'./data'",
    'train': False,
    'download': True,
    'transform': transform
  }

  p['testloader']['constraints'] = {
    'imports': imports,
    'cpu': 2,
    'mem': 30000000,
    'net': 10,
  }
  p['testloader']['fn'] = 'torch.utils.data.DataLoader(dataset,batch_size,shuffle,num_workers)'
  p['testloader']['params'] = {
    'dataset': { 'type': 'key', 'target': "p['testset']" },
    'batch_size': 4,
    'shuffle': False,
    'num_workers': 2
  }

  #generating the functions 
  s0 = 'trainset'
  s1 = 'trainloader'
  s2 = 'testset'
  s3 = 'testloader'
  # s4 = 'dataiter = iter(trainloader)'
  # s5 = 'images, labels = dataiter.next()'
  # s6 = ("print(' '.join('%5s' % classes[labels[j]] for j in range(4)))")

  #composing and returning the chain
  c = ([s0, s2],[s1, s3])

  print 'Sending chain:\n\ts0: {}\n\ts1: {}\n\ts2: {}\n\ts3: {}\n'.format(s0, s1, s2, s3)

  return c, p


#connects to the MLFV Module and sends the chain (c) with their parameters (p)
def send_chain(c,p):
  start = timeit.default_timer()

  rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
  con = rpyc.connect(MLFV_SERVER_HOST, MLFV_SERVER_PORT, config = rpyc.core.protocol.DEFAULT_CONFIG)

  ret = con.root.exec_chain(c,p)
  end = timeit.default_timer()
  time = end - start
  print("Total execution time: " + str(time))

  return ret


#executes a single chain
def single():
  c,p = get_chain()
  x = send_chain(c, p)


#perfoms multiple executions in parallel
def multiple(num_par):
  jobs = []
  c,p = get_chain()
  for i in range(num_par):
    print("Sending " + str(i))
    proc = multiprocessing.Process(target=send_chain, args=(c, p))
    jobs.append(proc)
    proc.start()
  for j in jobs:
    print("Waiting for jobs")
    j.join()
    print(j.name + 'exitcode = ' + str(j.exitcode))


if __name__ == "__main__":
  if (len(sys.argv) > 2):
    print("For executing a single chain, use: "+sys.argv[0]+"<filename>")
    print("For executing multiple chains in parallel, use: "+sys.argv[0]+" <num_par>")
    print("  where\n\t<num_par> = number of executions in parallel")
  elif len(sys.argv) == 1:
    single()
  else:
    multiple(sys.argv[1])

