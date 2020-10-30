import os
import sys
import rpyc
import time
import signal
import socket
import subprocess
from dependencies import install

client_ip=''
client_port=0

def verify_client_port(client_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',client_port))
    sock.close()
    if result == 0:
        return False
    else:
        return True


def signal_handler(sig, frame):
    global client_port
    info = [client_ip, client_port]
    con.root.unsubscribe(info)
    time.sleep(0.5)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python "+sys.argv[0]+" <server> <port> <dependencies> <libraries_to_be_shared> <memory_capacity> <cpu_count> <network_speed>")
        print("    eg.: python "+sys.argv[0]+" localhost 15089 \"numpy,pandas,sklearn\" \"os,sys,timeit,numpy,pandas,sklearn.ensemble,sklearn.preprocessing,sklearn.metrics\" 256m 2 100")
        # we opted for allowing these parameters manually for allowing the user to define how much processing capacity will be offered (and also to ease testing) 
        exit()

    dependencies = sys.argv[3]
    libs = sys.argv[4]
    cpu = sys.argv[5]
    mem = sys.argv[6]
    net = sys.argv[7]

    install(dependencies)

    signal.signal(signal.SIGINT, signal_handler)
    client_port = 18811

    while not verify_client_port(client_port):
        client_port+=1

    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
    try:
        con = rpyc.connect(sys.argv[1], sys.argv[2], config=rpyc.core.protocol.DEFAULT_CONFIG)
    except:
        print("ERROR: Could not connect to server "+sys.argv[1]+" on port "+str(sys.argv[2]))
        exit()

    client_ip = socket.gethostbyname(socket.getfqdn()) 

    info = [client_ip, client_port, libs, cpu, mem, net]
    print("Subscribed to "+sys.argv[1]+" on port "+str(sys.argv[2]))
    con.root.subscribe(info)

    subprocess.call("rpyc_classic.py -p "+str(client_port)+" --host 0.0.0.0 2> /dev/null", shell=True)


