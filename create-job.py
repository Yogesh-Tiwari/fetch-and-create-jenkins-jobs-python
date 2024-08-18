import jenkins
import json


with open('secrets.json','r') as file:
    config = json.load(file)

server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))

jobs=server.get_jobs()

for job in jobs:
    if(job["_class"]=='com.cloudbees.hudson.plugins.folder.Folder'):

        for childJob in job['jobs']:
            with open("{}.xml".format(childJob['name']),'w') as file:
                file.write(server.get_job_config("{}/{}".format(job['name'],childJob['name'])))
    else:
        with open("{}.xml".format(job['name']),'w') as file:
            file.write(server.get_job_config(job['name']))



# print(server.get_job_config('parent/multibranch-pipeline-child'))