import jenkins
import json
import os

with open('secrets/secret.json','r') as file:
    config = json.load(file)

server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))

jobs=server.get_jobs()
print(jobs)
os.makedirs('configs',exist_ok=True)

for job in jobs:
    if(job["_class"]=='com.cloudbees.hudson.plugins.folder.Folder'):
        os.makedirs("configs/{}".format(job['name']),exist_ok=True)

        with open("configs/{}/{}.xml".format(job['name'],job['name']),'w') as file:
            file.write(server.get_job_config(job['name']))
        
        for childJob in job['jobs']:
            with open("configs/{}/{}.xml".format(job['name'],childJob['name']),'w') as file:
                file.write(server.get_job_config("{}/{}".format(job['name'],childJob['name'])))
    
    else:
        with open("configs/{}.xml".format(job['name']),'w') as file:
            file.write(server.get_job_config(job['name']))

