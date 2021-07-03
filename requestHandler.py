from abc import ABC, abstractmethod
from utils import *
from Define import *




class RequestHandler(ABC):

    @abstractmethod
    def handle(self, msg):
        pass

class GPUSummaryRequestHandler(RequestHandler):

    def handle(self, msg=None):
        summary = get_gpu_summary()
        return summary



REQUEST_DISPATCHER = {
    COMMAND_ID.COMMAND_ID_GET_GPU_SUMMARY: GPUSummaryRequestHandler
}