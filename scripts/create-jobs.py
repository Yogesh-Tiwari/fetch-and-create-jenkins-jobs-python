import os
import jenkins
import json
from pathlib import Path
import glob

with open('secrets/secret.json','r') as file:
    config = json.load(file)


parentFolderName = 'config'
server = jenkins.Jenkins('http://localhost:8080',username=config.get('username'),password=config.get('password'))



def createJobsInFolder(folderPath):
    print(folderPath)
    for job in sortFilesAndFolders(folderPath):
        if (os.path.isfile(job)):
            with open(job,'r') as config:
                configXML = config.read()
                jobName = Path(job).stem
                jobURL = job.replace(f"{parentFolderName}\\","").replace(f"xml",'').replace("\\","/")[0:-1]
                server.create_job(jobURL,configXML)
        else:
            createJobsInFolder(job)





def sortFilesAndFolders(folderName):
    filesFirstFolderSecondList=[]
    filesList=[]
    foldersList=[]

    for file in os.listdir(folderName):
        filePath = os.path.join(folderName,file)
        if(os.path.isdir(filePath)):
            foldersList.append(filePath)
        elif os.path.isfile(filePath):
            filesList.append(filePath)

    filesFirstFolderSecondList = filesList+foldersList
    return filesFirstFolderSecondList


for job in sortFilesAndFolders(parentFolderName):
    print(job)
    if (os.path.isfile(job)):
        with open(job,'r') as config:
            configXML = config.read()
            jobURL = str(job).replace(f"{parentFolderName}\\","").replace(f"xml",'').replace("\\","/")[0:-1]
            server.create_job(jobURL,configXML)
    else:
        createJobsInFolder(job)





















# already_created_folders = set()
# def createJob(folderPath):
#     for file in os.listdir(folderPath):
#         filepath = Path(os.path.join(folderPath,file))
#         # print("fielpath at top :{} ".format(filepath))
#         if os.path.isdir(filepath):
#             # create parent folder job first
#             jobName = filepath.stem
#             search_pattern = os.path.join(filepath, "{}.xml".format(jobName))
#             file_path = glob.glob(search_pattern)

#             with open(file_path[0],'r') as config:
#                 configXML = config.read()
#                 # jobURL = file_path[0].replace("config\\","").replace("\\",'/').replace(jobName,"")
#                 jobURL = file_path[0].replace("config\\","").replace(f"{jobName}.xml",'').replace("\\","/")[0:-1]
#                 print(f"IF BLOCK: job being created with url: {jobURL} with name {jobName}")
#                 server.create_job(jobURL,configXML)
                
#             already_created_folders.add(file_path[0])

#             # print("filepath here is: {}".format(filepath))

#             for file in os.listdir(filepath):
#                 if f"{jobName}.xml" in file:
#                     continue;
                
#                 thisFilePath = os.path.join(filepath,file)

#                 if os.path.isdir(thisFilePath):
#                     print(f"IF BLOCK +++ : job being created with url: {jobURL} with name {jobName}")
#                     createJob(filepath)

#                 else:
#                     with open(thisFilePath,'r') as config:
#                         configXML = config.read()
#                         jobURL = str(thisFilePath).replace("config\\","").replace(".xml","").replace("\\","/")
#                         print(f"ELSE BLOCK--: job being created with url: {jobURL} with name {filepath.stem}")
#                         server.create_job(jobURL,configXML)
        
#         elif filepath in already_created_folders:
#             continue
            
#         else:
#             with open(filepath,'r') as config:
#                 configXML = config.read()
#                 jobURL = str(filepath).replace("config\\","").replace(".xml","").replace("\\","/")
#                 print(f"ELSE BLOCK: job being created with url: {jobURL} with name {filepath.stem}")
#                 server.create_job(jobURL,configXML)

            









#         #     for file in filesInFolder:
#         #         if os.path.isdir(file):
#         #             createJob("{}/{}".format(os.getcwd(),file))

#         #         elif file == "{}.xml".format(jobName):
#         #             with open(file,'r') as config:
#         #                 configXML = config.read()
#         #                 print("create job called with {}".format(jobName))
#         #                 server.create_job(jobName,configXML)
#         #         else:
#         #             with open(file,'r') as config:
#         #                 configXML = config.read()
#         #                 thisJobName = file.split('.')[0]
#         #                 print("create job called with {}".format(thisJobName))
#         #                 server.create_job("{}/{}".format(jobName,thisJobName),configXML)
#         #     os.chdir('..')
#         # else:
#         #     with open(filepath,'r') as config:
#         #             configXML = config.read()
#         #             thisJobName = file.split('.')[0]
#         #             print("create job called with {}".format(thisJobName))
#         #             server.create_job(thisJobName,configXML)




# createJob(parentFolderName)