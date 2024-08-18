import jenkins
import json
import os

with open('secrets/secret.json','r') as file:
    config = json.load(file)

server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))

parentFolderName = 'testing'

jobs=server.get_jobs()
print(jobs)
os.makedirs(parentFolderName,exist_ok=True)


def createJobsInFolder(parentFolderPath,jobs):
    for item in jobs:
        if(item["_class"]=='com.cloudbees.hudson.plugins.folder.Folder'):
            newPath = "{}/{}".format(parentFolderPath,item["name"])
            os.makedirs(newPath,exist_ok=True)

            with open("{}/{}.xml".format(newPath,item['name']),'w') as file:
                file.write(server.get_job_config(job['name']))

            createJobsInFolder(newPath,item['jobs'])
        else:
            with open("{}/{}.xml".format(parentFolderPath,item['name']),'w') as file:
                temp = parentFolderPath.replace("{}/".format(parentFolderName),"")
                file.write(server.get_job_config("{}/{}".format(temp,item['name'])))


for job in jobs:
    if(job["_class"]=='com.cloudbees.hudson.plugins.folder.Folder'):
        newPath = "{}/{}".format(parentFolderName,job['name'])
        
        # create new folder for the child jobs
        os.makedirs(newPath,exist_ok=True)

        # create folder .xml file
        with open("{}/{}.xml".format(newPath,job['name']),'w') as file:
            file.write(server.get_job_config(job['name']))

        createJobsInFolder(newPath,job['jobs'])
    else:
        with open("{}/{}.xml".format(parentFolderName,job['name']),'w') as file:
            file.write(server.get_job_config(job['name']))



