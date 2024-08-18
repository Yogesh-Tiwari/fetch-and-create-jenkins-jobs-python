import os
import jenkins
import json
from pathlib import Path
with open('secrets/secret.json','r') as file:
    config = json.load(file)

server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))


for file in os.listdir("configs"):
    filepath = Path(os.path.join("configs",file))
    print(filepath)
    print(file)
    if os.path.isdir(filepath):
        # create parent folder job first

        
    # jobName = filepath.stem
    # with open(filepath,'r') as config:
    #     configXML = config.read()
    
    # # create job
    # server.create_job(jobName,configXML)