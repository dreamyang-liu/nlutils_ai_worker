from abc import ABC, abstractmethod
from utils import *
from nlutils.Defines import *

__all__ = ['OPERATION_DISPATCHER']


class Operation(ABC):

    @abstractmethod
    def run(self, msg):
        pass

class InitWorkerOperation(Operation):

    def run(self, msg=None):
        default_logger.warn('IN OPERATION InitWorker')
        msg = dict()
        msg['command_id'] = COMMAND_ID.COMMAND_ID_WORKER_INITED
        default_logger.warn('OUT OPERATION InitWorker')
        return msg

class GPUSummaryOperation(Operation):

    def run(self, msg=None):
        msg = dict()
        msg['gpu_summary'] = get_gpu_summary()
        msg['command_id'] = COMMAND_ID.COMMAND_ID_UPDATE_GPU_SUMMARY_DONE
        return msg

class ServerLaunchWorkerTaskOperation(Operation):

    def run(self, msg=None):
        launch_task(msg['task_info'])
        return None

OPERATION_DISPATCHER = {
    OPERATION_ID.OPERATION_ID_INIT_WORKER: InitWorkerOperation,
    OPERATION_ID.OPERATION_ID_UPDATE_GPU_SUMMARY: GPUSummaryOperation,
    OPERATION_ID.OPERATION_ID_SERVER_LAUNCH_WORKER_TASK: ServerLaunchWorkerTaskOperation
}