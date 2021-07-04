import socket
import time
import json

from nlutils.Utils.Log import default_logger
from Configure import AIWConfigure
from Define import COMMAND_ID
from requestHandler import REQUEST_DISPATCHER

class AIWorkerSocketStore(object):

    def __init__(self, host=None, port=None):
        # self.socket.setblocking(0)
        self.alias = AIWConfigure.get_instance().get_config_info("ServerAlias")
        self.host = host
        self.port = port
    
    def create_pkg(self, msg_dict):
        msg_dict["worker_alias"] = self.alias
        msg_dict['timestamp'] = time.time()
        return msg_dict
    
    def seralize(self, pkg):
        return pkg.__str__().replace("'", '"').encode("utf-8")
                
    def handle(self, data):
        received_data = data.decode("utf-8")
        received_obj = json.loads(received_data)
        response = REQUEST_DISPATCHER[received_obj.get("command_id")].handle(received_obj)
        return response
    
    def init_worker(self):
        init_data = {
            "command_id": COMMAND_ID.COMMAND_ID_INIT_WORKER
        }
        response = REQUEST_DISPATCHER[init_data.get("command_id")].handle(init_data)
        return response
    
    def connect(self):
        if not hasattr(self, 'host') or not hasattr(self, 'port'):
            raise AttributeError("Host and port must be specified.")
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                msg = self.init_worker()
                msg = self.create_pkg(self, msg)
                buffer = self.seralize(msg)
                self.socket.sendall(buffer)
                default_logger.info(f"Connect AI server {self.host}:{self.port} success!")
                return
            except ConnectionRefusedError:
                pass
            except BrokenPipeError:
                pass
            except socket.error:
                default_logger.warn("Retrying to connect to AI server")
                time.sleep(2)
        
    def run(self):
        default_logger.warn(f"Recving data from AI server")
        while True:
            try:
                data = self.socket.recv(1024)
                msg = self.handle(data)
                msg = self.create_pkg(self, msg)
                buffer = self.seralize(msg)
                self.socket.sendall(buffer)
            except socket.error:
                default_logger.error("Cannot connect to AI server, retrying to connect")
                self.connect()
            except BrokenPipeError:
                default_logger.error("Cannot connect to AI server, retrying to connect")
                self.connect()
            except OSError:
                default_logger.error("Cannot connect to AI server, retrying to connect")
                self.connect()

    def close(self):
        self.socket.close()
    
if __name__ == '__main__':
    x = {
        'asdasfa': "afasfas"
    }
