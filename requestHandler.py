from abc import ABC, abstractmethod
from utils import *
from Define import *

__all__ = ['REQUEST_DISPATCHER']


class RequestHandler(ABC):

    @abstractmethod
    def handle(self, msg):
        pass

class InitWorkerRequestHandler(RequestHandler):

    def handle(self, msg=None):
        msg = dict()
        msg['operation_id'] = OPERATION_ID.OPERATION_ID_WORKER_INITED
        return msg

class GPUSummaryRequestHandler(RequestHandler):

    def handle(self, msg=None):
        msg = get_gpu_summary()
        msg['command_id'] = OPERATION_ID.OPERATION_ID_UPDATE_GPU_SUMMARY
        return msg


REQUEST_DISPATCHER = {
    COMMAND_ID.COMMAND_ID_INIT_WORKER: InitWorkerRequestHandler,
    COMMAND_ID.COMMAND_ID_GET_GPU_SUMMARY: GPUSummaryRequestHandler,
}