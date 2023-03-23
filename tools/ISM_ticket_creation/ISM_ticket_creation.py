import requests
import json
import time
import os
import toml
import zipfile
import csv
import pandas as pd
from datetime import date
from datetime import datetime
import logging

def incident_create(ism_url,ism_key,ism_attachment_url,final_directory,tag_name_list,flag_AH,assignee,assignee_desc,profile_link):
    Patches_list=[]
    Solution_list=[]
    VRR_group_list=[]
    VRR_list=[]
    Plugin_id_list=[]
    Asset_info_list=[]
    Scanner_name_list=[]
    Scanner_title_list=[]
    df_App = pd.read_csv(final_directory+"/Assets_"+str(tag_name_list)+".csv", low_memory=False)
    df_Host = pd.read_csv(final_directory+"/Findings_"+str(tag_name_list)+".csv", low_memory=False)
    df_multiple = pd.read_csv(final_directory+"/Ticket_Findings_"+str(tag_name_list)+".csv", low_memory=False)
    #print(assignee)
    for j in range(len(df_multiple.axes[0])):
        time.sleep(1)
        flag = False
        create = False
        #print(flag_AH)
        Scanner_name_list.append(df_multiple.iloc[j]['Scanner Name'])
        if(flag_AH == "A"):
            Plugin_id_list.append(df_multiple.iloc[j]["Scanner Plugin"])
            Asset_info_list.append(df_App.iloc[0]["Address"])
            
        elif(flag_AH == "H"):
            Plugin_id_list.append(df_multiple.iloc[j]["Scanner Plugin ID"])
            Asset_info_list.append(df_App.iloc[0]["IP Address"])
        Scanner_title_list.append(df_multiple.iloc[j]["Vulnerability"])    
        VRR_list.append(df_multiple.iloc[j]["Vulnerability Risk Rating"])
        VRR_group_list.append(df_multiple.iloc[j]["VRR Group"])
        Solution_list.append(df_multiple.iloc[j]['Possible Solution'])
        Patches_list.append(df_multiple.iloc[j]['Possible Patches'])
            
        payload = json.dumps({"Category": "Account Lockout","Impact": "Medium","Priority": "3","ProfileLink": profile_link,"Service": "Email Service","Source": "Phone","Status": "Active","Subject": "Scanner Name : " + ' , '.join(map(str, Scanner_name_list)) + "|" + " Scanner Plugin ID : " + ' , '.join(map(str, Plugin_id_list)) + "|" + " Scanner Title : " + ' , '.join(map(str, Scanner_title_list)) ,"Symptom": 'Plugin information : \n----------------------------\nPlugin ID : ' + ' , '.join(map(str, Plugin_id_list)) + "\n\nVRR : " + ' , '.join(map(str, VRR_list)) + "|"  + ' , '.join(map(str, VRR_group_list)) + "\n\n----------------------------------------------------------------------------------------------------\nAsset Information : \n----------------------------\n" + "Hostname : " + ' , '.join(map(str, Asset_info_list)) + "\n\nSolution : \n\n*) " + '\n*) '.join(map(str, Solution_list)) + "\n\nPatches : \n\n*) " + '\n*) '.join(map(str, Patches_list)),"Urgency": "Medium","Owner": assignee,"OwnerTeam": "Service Desk"})


    headers = {
      'Authorization': ism_key,
      'Content-Type': 'application/json',
      'Cookie': 'SID='
    }
    
    try:
        response = requests.request("POST", ism_url, headers=headers, data=payload)
    except Exception as e:
        print(e,response.text)
        logging.error(e,response.text)

    Rec_id_json = response.json()
    Rec_id = Rec_id_json["RecId"]
    Incident_num = Rec_id_json["IncidentNumber"]
    #print(Rec_id,Incident_num)


    ####### Attachment #######


    files = [('file', open(final_directory+"/Assets_"+str(tag_name_list)+".csv",'rb') ), ('file',open(final_directory+"/Ticket_Findings_"+str(tag_name_list)+".csv",'rb') )]
    payload={"ObjectID":Rec_id,"ObjectType":"incident#"}

    headers = {
      'Authorization': ism_key,
      'Cookie': 'SID='
    }

    response = requests.request("POST", ism_attachment_url, headers=headers, data=payload,files=files)
    if(response.status_code == 200):
        print("Incident is created and attachment is included...")
        logging.info("Incident is created and attachment is included...\n")
        print(assignee_desc)
        logging.info(assignee_desc)
        
    else:
        print("There is a problem in attaching the files to the ticket")
        logging.error("There is a problem in attaching the files to the ticket\n")
        print(assignee_desc)
        logging.info(assignee_desc)
    return Incident_num
