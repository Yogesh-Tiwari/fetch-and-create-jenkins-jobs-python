import jenkins
import json
import os
from typing import Dict, List
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def load_config(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_jenkins(config: Dict, skip_ssl_verification: bool = False) -> jenkins.Jenkins:
    session = jenkins.Jenkins(config.get('url'), 
                           username=config.get('username'), 
                           password=config.get('password'))
    if skip_ssl_verification:
        session._session.verify = False
        warnings.filterwarnings("ignore", category=InsecureRequestWarning) 
    return session

def create_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_job_config(server: jenkins.Jenkins, job_path: str, job_name: str, encoding: str = "utf-8") -> None:
    full_path = f"{job_path}.xml"
    with open(full_path, 'w', encoding=encoding ) as file:
        file.write(server.get_job_config(job_name))


def create_job(server: jenkins.Jenkins, job_url, config_xml):
    """Create a Jenkins job."""
    print(f"Creating/updating job: {job_url}")
    server.upsert_job(job_url, config_xml)