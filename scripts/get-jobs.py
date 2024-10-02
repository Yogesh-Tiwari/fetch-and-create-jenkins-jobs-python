import jenkins
import json
import os
from typing import List, Dict
from utils import *





def process_jobs(server: jenkins.Jenkins, parent_path: str, jobs: List[Dict], parent_name: str = '') -> None:
    for job in jobs:
        job_name = job['name']
        full_job_name = f"{parent_name}/{job_name}" if parent_name else job_name
        job_path = os.path.join(parent_path, job_name)

        if server.is_folder(full_job_name):
            create_folder(job_path)
            write_job_config(server, os.path.join(parent_path, job_name), full_job_name)
            process_jobs(server, job_path, job.get('jobs', []), full_job_name)
        else:
            write_job_config(server, os.path.join(parent_path, job_name), full_job_name)

def main():
    config = load_config('secrets/secret.json')
    server = connect_to_jenkins(config, skip_ssl_verification=False)
    parent_folder_name = config.get('config_folder')
    create_folder(parent_folder_name)
    jobs = server.get_jobs()
    # https://review.opendev.org/c/jjb/python-jenkins/+/719059 (install plugins error resolved PR link).
    # To find the installed plugin path, we need to use the following command: pip show python-jenkins.
    install_plugins(server, config.get('plugins', []))
    process_jobs(server, parent_folder_name, jobs)

if __name__ == "__main__":
    main()