"""Client class for connecting to the Logitech Harmony."""


import logging
import time
import socket
import select
import threading

LOGGER = logging.getLogger(__name__)


class HarmonyConnectionClient():
    
    def __init__(self, port):
        self.listenPort = port[0]
        
    def start_client_loop(self):
        """Retrieves the Harmony device configuration.

        Returns:
          A nested dictionary containing activities, devices, etc.
        """
        hostname = 'localhost'
        #hostname = '46.121.222.161'
        
        """need to reach the server from the internet"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, self.listenPort)) 
        s.setblocking(0)

        i = 0
        numberofpackets = 10
        while i < numberofpackets:
            start_time = time.time()
            s.send(bytes('tcp', 'UTF-8'))

            timeout_in_seconds = 10
            ready = select.select([s], [], [], timeout_in_seconds)
            if ready[0]:
                response = s.recv(1024)                
                print(response)
                print (time.time() - start_time)
            i = i + 1

        s.close()
        return
    
    def __del__(self):              
        print('Client finished')

def create_and_connect_tcp_client(port):
    client = HarmonyConnectionClient(port)
    client.start_client_loop()
    return



class ClientThread(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self._args = args
        #self._target = target
 
    def run(self):
        create_and_connect_tcp_client(*self._args)

