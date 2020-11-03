import os
import sys
import subprocess

def convert_memory(mem_value):
  if 'b' in mem_value:
    return mem_value.replace('b', '')
  if 'k' in mem_value:
    return mem_value.replace('k', 3 * '0')
  if 'm' in mem_value:
    return mem_value.replace('m', 6 * '0')
  if 'g' in mem_value:
    return mem_value.replace('g', 9 * '0')

  raise Exception('[MLFV-ERROR] Memory value is invalid! Value must contain \'b\', \'k\', \'m\' or \'g\' in order to inform its size.')


if __name__ == "__main__":
  if len(sys.argv) != 8:
    print 'Usage: python {} <server> <port> <dependencies> <libraries_to_be_shared> <memory_capacity> <cpu_count> <network_speed>'.format(sys.argv[0])
    print '    eg.: python {} localhost 15089 "numpy,pandas,sklearn" "os,sys,timeit,numpy,pandas,sklearn.ensemble,sklearn.preprocessing,sklearn.metrics" 256m 2 100'.format(sys.argv[0])
    # we opted for allowing these parameters manually to allow the user define how much processing capacity will be offered (and also to ease testing)
    exit()

  sys.argv.pop(0) # remove first argument (file name)
  try:

    server = sys.argv[0]
    port = sys.argv[1]
    dependencies = sys.argv[2]
    libs = sys.argv[3]
    mem = sys.argv[4]
    cpu = sys.argv[5]
    net = sys.argv[6]

    sys.argv[4] = convert_memory(sys.argv[4])

    # print 'docker run -ti {} mlfv/client python init_client.py {}'.format(' '.join(['--memory=' + mem, '--cpus=' + cpu]), ' '.join(sys.argv))

    subprocess.call('docker run -ti {} mlfv/client/gpu python init_client.py {}'.format(' '.join(['--memory=' + mem, '--cpus=' + cpu]), ' '.join(sys.argv)), shell=True)
  except Exception as e:
    print e
    exit()