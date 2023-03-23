#usr/bin/python
from datetime import datetime
import os
from random import sample
import sys
import shutil
import toml
import logging
import requests
import json
import glob
import dateutil.parser

pi,pe,pn,bi,be,bn = [],[],[],[],[],[]
pic = pec = pnc = bic = bec = bnc = count = 0 
def read_config_file(filename):
    
    try:
        toml_data = open(filename).read()
        data = toml.loads(toml_data)
       
    except FileNotFoundError:
        print("Wrong file or file path (or) Config file does not exist")
        logging.info("Wrong file or file path (or) Config file does not exist")
    return data      
 
def get_all_projects(jwt):
    limit=500
    offset=0
    url = "https://ivanti.polaris.synopsys.com/api/common/v0/projects?page%5Blimit%5D={}&page%5Boffset%5D={}".format(limit,offset)
    payload={}
    headers = {
    'Authorization': 'Bearer ' + jwt
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        json_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("String could not be converted to JSON")
        logging.info("String could not be converted to JSON")
    while 'https' in str(json_data['links']['next']):
        url=json_data['links']['next'] 
        payload={}
        headers = {
        'Authorization': 'Bearer ' + jwt
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        try:
            data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print("String could not be converted to JSON")
            logging.info("String could not be converted to JSON")
        json_data['data'] += data['data']
        json_data['links']= data['links']
    return json_data
    
    #obj=json.dumps(json_data)
    #with open('sample1.json','w') as f:
        #f.write(obj)    
        
def extract_upload(Condition,token,project,branch,file):
    
    global pi,pic,pe,pec,pn,pnc,bi,bic,be,bec,bn,bnc,count
    if(Condition == "C"):
        param = "--closed"
        print("==================================================== Getting Closed Issues for {0} project and {1} branch ====================================================\n".format(project,branch))
        logging.info("==================================================== Getting Closed Issues for {0} project and {1} branch ====================================================\n".format(project,branch))
    elif(Condition == "O"):
        param = "--opened" 
        print("==================================================== Getting Opened Issues for {0} project and {1} branch ====================================================\n".format(project,branch))   
        logging.info("==================================================== Getting Opened Issues for {0} project and {1} branch ====================================================\n".format(project,branch))        
    elif(Condition == "A"):
        param = "--all" 
        print("==================================================== Getting All Issues for {0} project and {1} branch ====================================================\n".format(project,branch))
        logging.info("==================================================== Getting All Issues for {0} project and {1} branch ====================================================\n".format(project,branch))
        
    try:
        os_cmd = "python getIssues.py --url https://ivanti.polaris.synopsys.com/ --token \"%s\" --project \"%s\" --branch \"%s\" \"%s\" --csv  > \"%s_%s\".csv" % (token,project,branch,param,file,count)
        
        if os.system(os_cmd) != 0:
            raise Exception('There might be some issues with the runs for the project\'s branch....')
    except:
        pe.append(project)
        pec+=1
        be.append(branch)
        bec+=1
        print("There might be some issues with the project\'s branch (or) There might be no runs for the project (or) The network connectivity might be interrupted, Please Check in Polaris GUI")
        logging.info("There might be some issues with the project\'s branch (or) There might be no runs for the project, Please Check in Polaris GUI")
        return pi,pic,pe,pec,pn,pnc,bi,bic,be,bec,bn,bnc
  
    file1 = open(str(file) +"_"+ str(count)+".csv")
    content = file1.readlines()
    file1.close()
    if("noissues" in content[0]):
        pn.append(project)
        bn.append(branch)
        pnc+=1
        bnc+=1
        print("The defined spec doesn't have any issues")
        logging.info("The defined spec doesn't have any issues")   
        os.remove(str(file) +"_"+ str(count)+".csv")
    elif("FATAL" in content[0]):
        os.remove(str(file) +"_"+ str(count)+".csv")
        pass
    else:
        shutil.copy(str(file) +"_"+ str(count)+".csv", 'upload_to_platform/files_to_process')
        print("The files are moved to upload section...Yet to be uploaded into Platform\n")
        logging.info("The files are moved to upload section...Yet to be uploaded into Platform\n")
        pi.append(project)
        bi.append(branch)
        pic+=1
        bic+=1
        os.remove(str(file) +"_"+ str(count)+".csv")
    count += 1    
       
    return pi,pic,pe,pec,pn,pnc,bi,bic,be,bec,bn,bnc
    
def getJwt(token):
    
    headers = {
        'accept': 'application/json',
    }
    data = {
        'accesstoken': token,
    }
    response = requests.post('https://ivanti.polaris.synopsys.com/api/auth/v1/authenticate', headers=headers, data=data)
    json_data = json.loads(response.text)
    return json_data["jwt"]

def getBranches_runs(branch_link,jwt):
    endpoint = branch_link + "?page%5Blimit%5D=500&page%5Boffset%5D=0"
    payload={}
    headers = {
      'Authorization': 'Bearer ' + jwt
    }
    response = requests.request("GET", endpoint, headers=headers, data=payload)
    try:
        json_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("String could not be converted to JSON")
        logging.info("String could not be converted to JSON")
        return pi,pic,pe,pec,pn,pnc,bi,bic,be,bec,bn,bnc
    return json_data

def dateCreated(projectId,branchId,jwt):
    #print(projectId)
    headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer ' + jwt
}

    params = {
    'filter[jobs][status][state]': 'COMPLETED',
    'filter[jobs][project][id]': projectId,
    'filter[jobs][branch][id]': branchId,
}

    response = requests.request("GET",'https://ivanti.polaris.synopsys.com/api/jobs/v2/jobs', params=params, headers=headers)
    #print(response.text,response.status_code)
    json_data = json.loads(response.text)
    #print(json_data)
    if(len(json_data["data"])!=0):
        return json_data["data"][0]["attributes"]["dateCreated"]
    else:
        return ''
      

def getbranchName(branchId,baseUrl,jwt):
    endpoint = baseUrl + '/api/common/v0/branches/' + branchId
    payload={}
    headers = {
      'Authorization': 'Bearer ' + jwt
    }
    response = requests.request("GET", endpoint, headers=headers, data=payload)
    try:
        json_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("String could not be converted to JSON")
        logging.info("String could not be converted to JSON")
        
    return json_data["data"]["attributes"]["name"]
    
if __name__ == '__main__':
    delta = ''
    analyzed_proj = []
    analyzed_branch = []
    Analyzed_dict = {}
    Condition = sys.argv[1]  
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'polaris.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)    
    logging.basicConfig(filename=log_file, level=logging.DEBUG,format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config_polaris.toml')
    logging.info("***** STARTING Polaris Ingestion Script *****\n")
    print("***** STARTING Polaris Ingestion Script *****\n")
    configuration = read_config_file(conf_file)
    token = configuration['polaris']['token']
    jwt = getJwt(token)
    
    url = "https://ivanti.polaris.synopsys.com"
    all_projects = get_all_projects(jwt)

    for j in range(len(all_projects["data"])):
        jwt = getJwt(token)
        file = configuration['polaris']['file']
        project = all_projects["data"][j]["attributes"]["name"]
        project_id = str(all_projects["data"][j]["id"])
        branch_link = all_projects["data"][j]["relationships"]["branches"]["links"]["self"]
        all_branches = getBranches_runs(branch_link,jwt)
        
        if(len(all_branches["data"])) == 0:
            print("\nThe project {0} doesn't have any branches\n".format(project))  
            logging.info(("\nThe project {0} doesn't have any branches\n".format(project)))  

        for k in range(len(all_branches["data"])):   
            branch_id = all_branches["data"][k]["id"]
            branch_name = getbranchName(branch_id,url,jwt)
            dateCreated_json = str(dateCreated(project_id,branch_id,jwt))
            #print(str(dateCreated_json))
            if(str(dateCreated_json) != ''):
                d = dateutil.parser.parse(str(dateCreated_json))
                job_date = d.strftime('%m/%d/%Y')
                #print(d.strftime('%m/%d/%Y')) 
                now = datetime.now()
                date_time_str = now.strftime("%m/%d/%Y")
                #print(date_time_str,job_date,type(date_time_str),type(job_date))
                d1 = datetime.strptime(date_time_str, "%m/%d/%Y")
                d2  = datetime.strptime(job_date, "%m/%d/%Y")
                delta = d1-d2
                #print(delta.days,type(delta)) 

                if(int(delta.days) <= 2 or int(delta.days) == 0):
                    analyzed_proj.append(project)
                    analyzed_branch.append(branch_name)
                    if project not in Analyzed_dict:
                        Analyzed_dict[project] = list()
                    Analyzed_dict[project].append(branch_name)
                    
                    print("Analyzed projects and branch",Analyzed_dict)
                    pi,pic,pe,pec,pn,pnc,bi,bic,be,bec,bn,bnc = extract_upload(Condition,token,project,branch_name,file)
                else:
                    print("\nThe project {0} and branch {1} wasnt analyzed for the last 2 days, Skipping...".format(project,branch_name))
                    logging.info("\nThe project {0} and branch {1} wasnt analyzed for the last 2 days, Skipping...".format(project,branch_name))    
            else:
                print("\nThere might be no runs for the project {0} (or) a newly created project".format(project))
                logging.info("\nThere might be no runs for the project {0} (or) a newly created project".format(project))

    path = os.getcwd() + "/upload_to_platform/files_to_process"
    allFiles = glob.glob(path + "/*.csv")
    allFiles.sort()
    with open(os.getcwd() + '/upload_to_platform/files_to_process/cumulative_upload_file.csv', 'wb') as outfile:
        for i, fname in enumerate(allFiles):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline() 
                shutil.copyfileobj(infile, outfile)

    for filename in allFiles:
        if("cumulative" in filename):
            print()
        else:    
            os.remove(filename)           
    execution3 = "python upload_to_platform/upload_to_platform.py"
    os.system(execution3)        
    print("\n***** The Ingestion is Done *****\n")
    logging.info("\n***** The Ingestion is Done *****\n")
    
    print("The Number of Project-Branch Combination ingested : {0}".format(pic))
    logging.info("\nThe Number of Project-Branch Combination ingested : {0}\n".format(pic))
    
    for c in range(len(bi)):
        print("\t| "+ pi[c] + " - " + bi[c])
        logging.info("\t| "+ pi[c] + " - " + bi[c])
        

    print("\n\nThe Number of Project-Branch combination that got exception : {0}".format(pec))
    logging.info("\n\nThe Number of Project-Branch combination that got exception : {0}".format(pec))
    logging.info("Analyzed project-branch combination are : {0}".format(Analyzed_dict))
    for a in range(len(pe)):
        print("\t| "+ pe[a] + " - " + be[a])
        logging.info("\t| "+ pe[a] + " - " + be[a])
        
    print("\nThe Number of Project-Branch combination that has no issues : {0}".format(pnc))
    logging.info("\nThe Number of Project-Branch combination that has no issues : {0}".format(pnc))
    
    for b in range(len(pn)):
        print("\t| "+ pn[b] + " - " + bn[b])
        logging.info("\t| "+ pn[b] + " - " + bn[b])
    
