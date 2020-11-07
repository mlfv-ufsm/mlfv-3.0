import rpyc.core.protocol
import sys
import signal
from MLFV_Parsing import parse_chain
from MLFV_DB import insert_reg, remove_reg, create_db
from rpyc.utils.server import ThreadedServer as Server


db = None
port_chain = 15088
port_cli = 15089


class ReceiveChain(rpyc.Service):
    def on_connect(self,x):
        print("Chain received")
    def on_disconnect(self,x):
        print("Chain ended")
    def exposed_exec_chain(self, c, p):
        x = parse_chain(c, p, db)
        return x


class ReceiveClient(rpyc.Service):
    def exposed_subscribe(self, info):
        insert_reg(db, {
            'ip': info[0],
            'port': info[1],
            'libs': info[2],
            'cpu': info[3],
            'mem': info[4],
            'net': info[5],
            'gpu': info[6]
        })
        print("Host " + str(info[0]) + ":" + str(info[1]) + " subscribed")
    def exposed_unsubscribe(self, info):
        remove_reg(db, {'ip': info[0], 'port': info[1]})
        print("Host " + str(info[0]) + ":" + str(info[1]) + " unsubscribed")


if __name__ == "__main__":
    rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

    db = create_db()

    print("Starting chain receiver at port "+str(port_chain))
    server_chain = Server(ReceiveChain, port=port_chain, backlog=10, protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    server_chain._start_in_thread()

    print("Starting client receiver at port "+str(port_cli))
    server_cli = Server(ReceiveClient, port=port_cli, backlog=10, protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    server_cli.start()
