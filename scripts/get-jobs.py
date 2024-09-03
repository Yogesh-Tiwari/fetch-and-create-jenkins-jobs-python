import jenkins
import json
import os
from typing import List, Dict

def load_config(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_jenkins(config: Dict) -> jenkins.Jenkins:
    return jenkins.Jenkins(config.get('url'), 
                           username=config.get('username'), 
                           password=config.get('password'))

def create_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_job_config(server: jenkins.Jenkins, job_path: str, job_name: str) -> None:
    full_path = f"{job_path}.xml"
    with open(full_path, 'w') as file:
        file.write(server.get_job_config(job_name))

def get_plugins(server: jenkins.Jenkins) -> List[Dict]:
    return server.get_plugins()

def install_plugins(server: jenkins.Jenkins, plugins: List) -> None:
    for plugin in plugins:
        server.install_plugin(plugin, include_dependencies=True)

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
    server = connect_to_jenkins(config)
    parent_folder_name = config.get('config_folder')
    create_folder(parent_folder_name)
    jobs = server.get_jobs()
    # https://review.opendev.org/c/jjb/python-jenkins/+/719059 (install plugins error resolved PR link).
    # To find the installed plugin path, we need to use the following command: pip show python-jenkins.
    install_plugins(server, config.get('plugins', []))
    process_jobs(server, parent_folder_name, jobs)

if __name__ == "__main__":
    main()