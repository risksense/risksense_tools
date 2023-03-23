from distutils.command.config import config
from functionCalls_Changing import *
import os,logging
from conf.config import *
import requests, pandas as pd, numpy as np, json, warnings, datetime
from datetime import date
import math
# from azure.devops.connection import Connection
warnings.simplefilter("ignore")

exportName = "Findings"
fileName = "Client_"+str(clientID)+"_"+exportName
currentDate = datetime.datetime.now()
today = date.today()
date_1 = datetime.datetime.strptime(str(today), "%Y-%m-%d")

expiry_date = str(date_1 + datetime.timedelta(days=90))[0:10]
currentTime = currentDate.strftime("%H:%M:%S")

header = {
     "content-type": "application/json",
     "x-api-key": apiToken
    }

def mainFunction():

    # Logging part 

    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'ADO_ticket_creation.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)    
    logging.basicConfig(filename=log_file, level=logging.DEBUG,format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    print("**** STARTING THE ADO Ticket Creation SCRIPT ****\n")
    logging.info("**** STARTING THE ADO Ticket Creation SCRIPT ****\n")
    config_dict = {}
    for app in range(len(df_grp_sev.values)):
        # group_idd = int(df_group_id["Group ID"][app])
        # print(num1)
        group_id = str(df_group_id["Group ID"][app]).split('.')[0]
        # print(group_id)
        list = [df_project["Project"][app],df_instance["Instance"][app],df_token["Token"][app],df_user["User"][app],df_area["Area"][app],df_iteration["Iteration"][app],df_sev["Severity"][app],group_id]
        config_dict[df_grp_sev["Group_sev"][app]] = list
         
    # print(config_dict)

    for app in config_dict.keys():
        # print(app) 
        print("\nExporting '{}' Application Findings...\n".format(app))
        logging.info("\nExporting '{}' Application Findings...\n".format(app))
        app_name_list = app_level_grouping(config_dict[app][7],config_dict[app][6])
        # print(app_name_list)
    # df = pd.read_excel("Blackduck_proj_grouping.xlsx", sheet_name=0)
    # app_name_list = df['BlackDuck Project name'].tolist()
    # # print(app_name_list)
        for app_name in range(len(app_name_list)):
            # jsonified_result = groupby(app_name_list[app_name])
            jsonified_result = groupby_new(app_name_list[app_name],config_dict[app][6])
            for scanner_plugin in range (len(jsonified_result["data"])):
                scanner_plugin_name = jsonified_result["data"][scanner_plugin]["App Finding Scanner Plugin"]
                print("\n[+]  Application '{}' , Scanner Plugin '{}' ({}/{}) is being exported for ticket creation...".format(app_name_list[app_name],scanner_plugin_name,scanner_plugin+1,len(jsonified_result["data"])))
                logging.info("\n[+]  Application '{}' , Scanner Plugin '{}' ({}/{}) is being exported for ticket creation...".format(app_name_list[app_name],scanner_plugin_name,scanner_plugin+1,len(jsonified_result["data"])))
                export(scanner_plugin_name,app_name_list[app_name],config_dict[app][6])
                Blackduck_projectname =  app_name_list[app_name]
                url = add_url(Blackduck_projectname,scanner_plugin_name)
                print("\n[+]  Reading the exported scanner plugin info file...")
                logging.info("\n[+]  Reading the exported scanner plugin info file...")
                # Reading the exported file from Risksense and gathering metrics for the ticket creation
                try:
                    df = pd.read_csv("Findings/Findings.csv", low_memory=False)
                    CVE_list=[]
                    # app_list = df["App Name"].values.tolist()
                    app_list = df["App Name"].astype(str).str.strip().unique().tolist()
                    print(app_list)
                    app_list = ", ".join(app_list)
                    location_list = df["Location"].astype(str).str.strip().unique().tolist()
                    location_list = ", ".join(location_list)
                    CWE_list1 = df["CWE ID"].astype(str).str.strip().unique().tolist()   
                    CVE_list = df["CVEs Associated"].astype(str).str.strip().unique().tolist()
                    CWE_list1 = ", ".join(CWE_list1) 
                    CVE_list= ", ".join(CVE_list)       
                    # print(location_list)
                except pd.errors.EmptyDataError:
                    print("\n[+] The exported information for the {} is empty. Please check the application name provided in config.xlsx file".format(app))
                    logging.error("\n[+] The exported information for the {} is empty. Please check the application name provided in config.xlsx file".format(app))
                    print("-----------------------------------------------------------------------------------------------------------")
                    logging.info("-----------------------------------------------------------------------------------------------------------")
                    continue # will skip the rest of the block and move to next file
                    
                df['App Name'] = df['App Name'].replace(np.nan,"Not Available")
                df['Due Date'] = df['Due Date'].replace(np.nan,"Not Available")
                df['Possible Solution'] = df['Possible Solution'].replace(np.nan,"Not Available")
                df['Possible Patches'] = df['Possible Patches'].replace(np.nan,"Not Available")
                df['Description'] = df['Description'].replace(np.nan,"Not Available")
                df['CWE ID'] = df['CWE ID'].replace(np.nan,"")
                df['CVEs Associated'] = df['CVEs Associated'].replace(np.nan,"")
                df['Location'] = df['Location'].replace(np.nan,"Not Available")
                df['CVSS 3.0'] = df['CVSS 3.0'].replace(np.nan,"")
                df['CVSS 3.0 Vector'] = df['CVSS 3.0 Vector'].replace(np.nan,"")
                df['OWASP'] = df['OWASP'].replace(np.nan,"Not Available")
                df['Scanner Name'] = df['Scanner Name'].replace(np.nan,"Not Available")
                df['Vulnerability'] = df['Vulnerability'].replace(np.nan,"Not Available")
                df['Vulnerability Risk Rating'] = df['Vulnerability Risk Rating'].replace(np.nan,"") 
                
                df['VRR Group'] = df['VRR Group'].replace(np.nan,"")
                df['Due Date'] = df['Due Date'].replace(np.nan,"Not Available")
                df['Scanner Output'] = df['Scanner Output'].replace(np.nan,"Not Available")
                
                TotalAppFindings = df.shape[0]
                print("\n[+] Total AppFindings without ticket creation is",TotalAppFindings)
                #logging.info("\n[+] Total AppFindings without ticket creation is",TotalAppFindings)
                
                userID =  get_userId()
                print("\n[+] User ID is {}".format(userID))

                
                count = 0
                    
                # Iterating through each row to create ticket per finding
                # print(TotalAppFindings)
                for j in range(TotalAppFindings):
                    scanner_link_app = str(app_name_list[app_name]).replace(" ","%20")
                    for k in range(1):
                        CWE = ''
                        flag = 0
                        id = df.iloc[k]["Id"]
                        uniqueVulnerability = df.iloc[k]["Vulnerability"]
                        scannerplugin = str(df.iloc[k]["Scanner Plugin"])[10:]
                        # print(scannerplugin)
                        scanner_link = 'https://ivanti.app.blackduck.com/api/vulnerabilities/{}/affected-projects?sortField=project.name%2C%20release.version&ascending=true&offset=0&q={}'.format(scannerplugin,str(scanner_link_app))
                    CWE = ''
                    id = df.iloc[j]["Id"]
                    uniqueVulnerability = df.iloc[j]["Vulnerability"]
                    #scannerplugin = df.iloc[j]["Scanner Plugin"]

                    # df['CWE ID'] = df['CWE ID'].astype(str)
                    CWE  = CWE_list1
                    AppName= app_list
                    OWASP = df.iloc[j]["OWASP"]
                    CVSS3score = df.iloc[j]["CVSS 3.0"]
                    CVSS3vector = df.iloc[j]["CVSS 3.0 Vector"]
                    VRR = df.iloc[j]["Vulnerability Risk Rating"]
                    #print(type(VRR))
                    Due_date = df.iloc[j]["Due Date"]
                    Scanner_output = df.iloc[j]["Scanner Output"]
                    Title = "SID - " + str(id) + " : " + str(uniqueVulnerability)
                    SolutionString = str(df.iloc[j]["Possible Solution"]).replace("\"","")
                    PatchString = str(df.iloc[j]["Possible Patches"]).replace("\"","")
                    Description = df.iloc[j]["Description"]
                    CVEs=str(CVE_list)
                    Location= str(location_list)
                    # print("Location : "+Location)
                    VRR_group = df.iloc[j]["VRR Group"]
                    Scanner_Name = df.iloc[j]["Scanner Name"]
                    Scanner_Name_org = Scanner_Name
                    if("polaris" in Scanner_Name.lower()):
                        Scanner_output = df.iloc[j]["Scanner Output"]
                    else:
                        Scanner_output = ""

                ado_template_fields = ado_template(config_dict,app)   
                #print(ado_template_fields) 
                RAS,CVSS_sev,Scanner_Name,Priority_group = rs_ADO_field_data(VRR_group,CVSS3score,Scanner_Name,ado_template_fields)
            # Tag creation and fetch its ID from Risksense
                count = count+1
                tagName = str(id) + "  Dated: " + datetime.date(day=currentDate.day, month=currentDate.month, year=currentDate.year).strftime('%d %B %Y') + " " + currentTime + " Ticket - " + str(count)
                filter_tagCreation = {
                    "fields":[
                        {
                        "uid":"TAG_TYPE",
                        "value":"REMEDIATION"
                        },
                        {
                        "uid":"NAME",
                        "value":tagName
                        },
                        {
                        "uid":"DESCRIPTION",
                        "value":""
                        },
                        {
                        "uid":"OWNER",
                        "value":userID
                        },
                        {
                        "uid":"COLOR",
                        "value":"#648d9f"
                        },
                        {
                        "uid":"LOCKED",
                        "value":False
                        },
                        {
                        "uid":"PROPAGATE_TO_ALL_FINDINGS",
                        "value":True
                        }
                    ]
                    }

                tagCreation_resp = requests.post("https://{}.risksense.com/api/v1/client/{}/tag".format(platform,clientID),headers=header,json=filter_tagCreation)
                if tagCreation_resp.status_code == 201:
                    tagCreation_resp_json = json.loads(tagCreation_resp.text)
                    tagID = tagCreation_resp_json['id']
                    print("\n[+] Form for the ticket creation has been filled and tag is created Successfully!. The Tag ID is: {}".format(tagID))
                    logging.info("\n[+] Form for the ticket creation has been filled and tag is created Successfully!. The Tag ID is: {}".format(tagID))
                else:
                    print("\n[+] Failure!, tag is not created. Reason : {}".format(tagCreation_resp.text))
                    logging.error("\n[+] Failure!, tag is not created. Reason : {}".format(tagCreation_resp.text))
                    
                    break

            # Ticket creation in ADO with the fields from RS
                
                response = ado_app_ticket_creation(config_dict,uniqueVulnerability,app,Title,Priority_group,Scanner_Name,CVSS3score,CVSS3vector,CWE,VRR,Scanner_Name_org,Description,Location,SolutionString,PatchString,OWASP,RAS,CVSS_sev,AppName,
                scanner_link,url,expiry_date,CVEs)

                json_response = json.loads(response.text)   
                
                # print(json_response)
                # print(config_dict,app)
                ADO_ticket_id = json_response["data"]["ms.vss-work-web.update-work-items-data-provider"]["data"][0]["id"]
                #Attaching findings CSV file
                # print("Attaching file")
                # attach_findings(config_dict,ADO_ticket_id,app)


                if(response.status_code == 200 and ADO_ticket_id != -2 ):
                    print("\n[+] The ticket {} for the application {} is created in ADO for the area {} and iteration {} in the project {} , instance {}...".format(ADO_ticket_id,app,config_dict[app][4],config_dict[app][5],config_dict[app][0],config_dict[app][1]))
                    logging.info("\n[+] The ticket {} for the application {} is created in ADO for the area {} and iteration {} in the project {} , instance {}...".format(ADO_ticket_id,app,config_dict[app][4],config_dict[app][5],config_dict[app][0],config_dict[app][1]))
                else:
                    print("\nThere's a problem with the ticket creation in the area {} and in the iteration {} and the reason is {}".format(config_dict[app][4],config_dict[app][5],json_response["data"]["ms.vss-work-web.update-work-items-data-provider"]["data"][0]["error"]["message"]))
                    logging.error("\nThere's a problem with the ticket creation in the area {} and in the iteration {} and the reason is {}".format(config_dict[app][4],config_dict[app][5],json_response["data"]["ms.vss-work-web.update-work-items-data-provider"]["data"][0]["error"]["message"]))
                    break

            # Changing tag name after ticket creation

                url = "https://{}.risksense.com/api/v1/client/{}/admin/tag/{}".format(platform,clientID,tagID)
                
                headers = {
                'accept': 'application/json',
                'x-api-key': apiToken,
                }

                json_data = { 'fields': [ { 'uid': 'TAG_TYPE', 'value': 'REMEDIATION', }, { 'uid': 'NAME', 'value': str(ADO_RS_tag) + str(ADO_ticket_id) , }, { 'uid': 'DESCRIPTION', 'value': 'ADO Tag', }, { 'uid': 'OWNER', 'value': tagowner, }, { 'uid': 'COLOR', 'value': '#648d9f', }, { 'uid': 'LOCKED', 'value': False, }, { 'uid': 'PROPAGATE_TO_ALL_FINDINGS', 'value': True, }, ], }
                
                response = requests.put(url, headers=headers, json=json_data)

                if(response.status_code == 200 ):
                    print("\n[+] Change tag is done...Now , you have the tag '{0}' is renamed to '{1}' in Risksense platform...\n".format(tagName,str(ADO_RS_tag)+str(ADO_ticket_id)))
                    logging.info("\n[+] Change tag is done...Now , you have the tag '{0}' is renamed to '{1}' in Risksense platform...\n".format(tagName,str(ADO_RS_tag)+str(ADO_ticket_id)))
                    
                else:
                    print("\n[+] The Ticket is created but the tag is not renamed in RS and the reason is {}".format(response.text))
                    logging.error("\n[+] The Ticket is created but the tag is not renamed in RS and the reason is {}".format(response.text))
                    break


            # Adding a note to RS Finding with the ticket creation link
                AppFindingID = str(df.iloc[j]["Id"])

                json_data = {
                'filterRequest': {
                    'filters': [
                        {
                            'field': 'id',
                            'exclusive': False,
                            'operator': 'IN',
                            'value': AppFindingID,
                        },
                    ],
                },
                'note': "https://{}/{}/_workitems/edit/{}/".format(config_dict[app][1],config_dict[app][0],ADO_ticket_id)
            }

                response = requests.post('https://{}.risksense.com/api/v1/client/{}/applicationFinding/note'.format(platform,clientID),headers=headers,json=json_data)
                if(response.status_code == 200):
                    print("[+] Added Note to the Finding successfully with the link")
                    logging.info("[+] Added Note to the Finding successfully with the link")
                else:
                    print(" The note is not added. The reason is {}".format(response.text))
                    logging.error(" The note is not added. The reason is {}".format(response.text))


            # Tag assignment in RS and sync its value with ADO field
                
                filter_ticketAttachment = {"tagId":tagID,"isRemove":False,"filterRequest":{"filters":[{"field":"id","exclusive":False,"operator":"IN","value":AppFindingID}]},"publishTicketStats":True}

                ticketAttachment_resp =  requests.post("https://{}.risksense.com/api/v1/client/{}/search/applicationFinding/job/tag".format(platform,clientID),headers=header,json=filter_ticketAttachment)
                if ticketAttachment_resp.status_code == 200:
                    print("\n[+] Attachment is attached in the created ticket successfully!")
                    logging.info("\n[+] Attachment is attached in the created ticket successfully!")
                    print("==========================================================================================================\n")
                    logging.info("==========================================================================================================\n")
                else:
                    print("\n[+] Failure!, Attachment is not attached in the created ticket. Reason : {}".format(ticketAttachment_resp.text))
                    logging.error("\n[+] Failure!, Attachment is not attached in the created ticket. Reason : {}".format(ticketAttachment_resp.text))
                    break

if __name__ == "__main__":
    mainFunction()