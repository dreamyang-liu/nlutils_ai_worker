import os
import time
import subprocess
from Configure import *
from nlutils.Utils.Log import default_logger
from EmailUtils import default_email_manager
    
def get_gpu_summary():
    summary = dict()
    gpu_memos = subprocess.getoutput(r"nvidia-smi | grep 'MiB' | awk '{print $9, $11}' | grep -v '|'").splitlines()
    gpu_statuses = subprocess.getoutput(r"nvidia-smi | grep 'Off' | awk '{print $2, $6}' | grep -v '|'").splitlines()
    for gpu_status, gpu_memo in zip(gpu_statuses, gpu_memos):
        gpu_id, status = gpu_status.split(' ')
        used_memoary, total_memoary = map(lambda x:int(x), gpu_memo.replace('MiB', '').split(' '))
        summary[int(gpu_id)] = {
            "status": status,
            "used_memoary": used_memoary,
            "total_memoary": total_memoary,
            "available_memory": total_memoary - used_memoary
        }
    return summary


def launch_task(task_info):
    try:
        task_repo_url = task_info.get("repo_url")
        task_repo_name = task_info.get("repo_name")
        local_repo_root_path = AIWConfigure.get_instance().get_config_info('LocalRepoPath').as_string()
        local_repo_path = f'{local_repo_root_path}/{task_repo_name}'
        local_repo_path = os.path.abspath(local_repo_path)
        if os.path.isdir(local_repo_path):
            default_logger.warn('Repo already exists in local folder !')
            if AIWConfigure.get_instance().get_config_info("ForceUpdate").as_bool():
                default_logger.warn('Force updating local repo.')
                os.system(f'rm -rf {local_repo_path}')
                os.system(f"git clone {task_repo_url} {local_repo_path}")
            else:
                default_logger.info('Updating local repo using git pull..')
                os.system(f'cd {local_repo_path} && git pull')
        else:
            default_logger.info('Cloning repo to local folder...')
            os.system(f"git clone {task_repo_url} {local_repo_path}")
        launch_cmd = f'cd {local_repo_path} &&'
        launch_cmd += f'bash {task_info.get("launch_script")} {task_info.get("assigned_gpu_id")} '
        launch_cmd += f'{task_info.get("args")}'
        subprocess.run(launch_cmd, check=True)
        email_msg = f"Your Task {task_repo_name} assigned to server {task_info.get('assigned_server')} has finished, you can check it now."
        default_email_manager.send_to(task_info.get("email"), email_msg, f"NLUTILS:[AI TASK DONE] --- {task_repo_name} --- {task_info.get('assigned_server')}")
    except (subprocess.CalledProcessError, Exception) as e:
        email_msg = f"Your Task {task_repo_name} assigned to server {task_info.get('assigned_server')} has failed due to {e.__str__()}, please resubmit your task later."
        default_email_manager.send_to(task_info.get("email"), email_msg, f"NLUTILS:[AI TASK FAILED] --- {task_repo_name} --- {task_info.get('assigned_server')}")

if __name__ == '__main__':
    task_info = {
        "repo_name": "fix",
        "repo_url": "https://github.com/leonard-thong/SciAnnotate.git",
        "timestamp": time.time(),
        "args": "",
        "estimate_cpu_memory": 8000,
        "estimate_gpu_memory": 8000,
        "assigned_gpu_id": 1,
        "assigned_server": "local",
        "launch_script": "train.sh",
        "email": "mliu444@gatech.edu"
    }
    launch_task(task_info)