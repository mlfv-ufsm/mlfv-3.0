#https://gnocchi.nodead.net/index.html

import json
import shade
import os
import datetime
import uuid
import sys
import time

from keystoneauth1.identity import v3
from keystoneauth1 import session
from gnocchiclient.v1 import client
from gnocchiclient import auth
from gnocchiclient.v1 import client

class Gnocchi():
    def __init__(self, cloud_name):
        self.cloud = shade.openstack_cloud(cloud=cloud_name)
        self.auth_dict = self.cloud.auth
        #Import credentials witch clouds.yml
        self.auth = v3.Password(auth_url=str(self.auth_dict['auth_url']),
                           username=str(self.auth_dict['username']),
                           password=str(self.auth_dict['password']),
                           project_name=str(self.auth_dict['project_name']),
                           user_domain_id=str(self.auth_dict['user_domain_id']),
                           project_domain_id=str(self.auth_dict['project_domain_id']))
        self.sess = session.Session(auth=self.auth)
        #Open a session with credentials clouds.yml
        self.gnocchi_client = client.Client(session=self.sess)
    
    def get_metric(self,metric,start,stop,resource_id,granularity):
        meters = self.gnocchi_client.metric.get_measures(str(metric),
                                                           start=start,
                                                           stop=stop,
                                                           resource_id=resource_id,
                                                           granularity=granularity)
        if len(meters) == 0:
            return -1
        sum = 0
        for item in meters:
            sum += item[2]
        
        return sum/len(meters)
    
    def get_list_meters(self,resource_id):
        list_meters = self.gnocchi_client.resource.get(resource_type='generic',resource_id=resource_id)
        return list_meters['metrics']
    
    def get_bandwidth(self,start,stop,link_id,granularity):
        meters = self.gnocchi_client.metric.get_measures('bandwidth',
                                                           start=start,
                                                           stop=stop,
                                                           resource_id=link_id,
                                                           granularity=granularity)
        if len(meters) == 0:
            return -1
        sum = 0
        for item in meters:
            sum += item[2]
        
        return sum/len(meters)
    

def get_host_info(host, time=10, link_id): # time in seconds
    auth_plugin = auth.GnocchiBasicPlugin(user="id-user",endpoint="ip-address:8041")
    gnocchi = client.Client(session_options={'auth': auth_plugin})

    cloud = Gnocchi('nerdstack')

    stop = datetime.datetime.utcnow()
    start = (stop - datetime.timedelta(seconds=int(time))

    cpu = cloud.get_metric('cpu_util', host, start.isoformat(), stop.isoformat(), 1)
    memory = cloud.get_metric('memory.usage', host, start.isoformat(), stop.isoformat(), 1)

    interface_bytes_in = cloud.get_metric('network.incoming.bytes.rate', host, start.isoformat(), stop.isoformat(), 1)
    interface_bytes_out = cloud.get_metric('network.outgoing.bytes.rate', host, start.isoformat(), stop.isoformat(), 1)
    interface_packets_in = cloud.get_metric('network.incoming.packets.rate', host, start.isoformat(), stop.isoformat(), 1)
    interface_packets_out = cloud.get_metric('network.outgoing.packets.rate', host, start.isoformat(), stop.isoformat(), 1)

    bandwidth = cloud.get_bandwidth(start.isoformat(), stop.isoformat(), link_id, 1)

    bandwidth = bandwidth*8/1048576
    return (cpu, memory, bandwidth)

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] == "-h":
        print(" - Usage: ./agent-gnocchi.py [OpenStack-VM-ID] [time-of-capture-in-seconds] [link_id]")
    main()

