import os
import jenkins
import json
from pathlib import Path

with open('secrets/secret.json','r') as file:
    config = json.load(file)

parentFolderName = 'config'
server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))


def createJob(folderPath):
    for file in os.listdir(folderPath):
        filepath = Path(os.path.join(folderPath,file))
        if os.path.isdir(filepath):
            # create parent folder job first
            os.chdir(filepath)
            jobName = filepath.stem

            filesInFolder = os.listdir(os.getcwd())

            # temporary creating list of the files
            for file in os.listdir(os.getcwd()):
                if file == "{}.xml".format(jobName):
                    filesInFolder.remove(file)
                    filesInFolder.insert(0,file)

            for file in filesInFolder:
                if os.path.isdir(file):
                    createJob("{}/{}".format(os.getcwd(),file))
                elif file == "{}.xml".format(jobName):
                    with open(file,'r') as config:
                        configXML = config.read()
                        print("create job called with {}".format(jobName))
                        server.create_job(jobName,configXML)
                else:
                    with open(file,'r') as config:
                        configXML = config.read()
                        thisJobName = file.split('.')[0]
                        print("create job called with {}".format(thisJobName))
                        server.create_job("{}/{}".format(jobName,thisJobName),configXML)
            os.chdir('..')
        else:
            with open(filepath,'r') as config:
                    configXML = config.read()
                    thisJobName = file.split('.')[0]
                    print("create job called with {}".format(thisJobName))
                    server.create_job(thisJobName,configXML)




createJob(parentFolderName)