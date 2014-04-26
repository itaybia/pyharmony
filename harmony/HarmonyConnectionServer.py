"""Client class for connecting to the Logitech Harmony."""


import logging
import socket
import select
import threading

LOGGER = logging.getLogger(__name__)

 

class HarmonyConnectionServer():
    
    def __init__(self, port):
        self.running = True
        self.listenPort = port[0]

    """need to change to allow more than one connection. also need password of some sort"""
    def start_server_loop(self):
        #for tcp
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", self.listenPort)) 
        s.listen(1)
        sock, addr = s.accept() 
        sock.setblocking(0)
        
        while self.running:
            timeout_in_seconds = 10
            ready = select.select([sock], [], [], timeout_in_seconds)
            if ready[0]:
                data = sock.recv(1024)
                sock.send(data)
        
        s.close()
        return
    
    def __del__(self):              
        print('Server finished')

"""
def create_and_connect_tcp_server(port):
    server = HarmonyConnectionServer(port)
    server.start_server_loop()
    return server
"""



class ServerThread(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.server = HarmonyConnectionServer(*args)
        #self._target = target
 
    def run(self):
        self.server.start_server_loop()
    
    def stop_server_loop(self):
        self.server.running = False
        return
