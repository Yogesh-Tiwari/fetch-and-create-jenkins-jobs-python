import jenkins
import json
import os
from typing import List, Dict

def load_config(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_jenkins(config: Dict) -> jenkins.Jenkins:
    return jenkins.Jenkins('http://localhost:8080', 
                           username=config.get('username'), 
                           password=config.get('password'))

def create_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_job_config(server: jenkins.Jenkins, job_path: str, job_name: str) -> None:
    full_path = f"{job_path}.xml"
    with open(full_path, 'w') as file:
        file.write(server.get_job_config(job_name))

def process_jobs(server: jenkins.Jenkins, parent_path: str, jobs: List[Dict], parent_name: str = '') -> None:
    for job in jobs:
        job_name = job['name']
        full_job_name = f"{parent_name}/{job_name}" if parent_name else job_name
        job_path = os.path.join(parent_path, job_name)

        if job["_class"] == 'com.cloudbees.hudson.plugins.folder.Folder':
            create_folder(job_path)
            write_job_config(server, os.path.join(parent_path, job_name), full_job_name)
            process_jobs(server, job_path, job.get('jobs', []), full_job_name)
        else:
            write_job_config(server, os.path.join(parent_path, job_name), full_job_name)

def main():
    config = load_config('secrets/secret.json')
    server = connect_to_jenkins(config)
    parent_folder_name = 'config'
    create_folder(parent_folder_name)
    jobs = server.get_jobs()
    process_jobs(server, parent_folder_name, jobs)

if __name__ == "__main__":
    main()