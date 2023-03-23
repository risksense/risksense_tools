#!/usr/bin/python
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
import shutil
import ISM_ticket_creation as ISM
import logging
import argparse

time_today = time.time()

def read_config_file(filename):
    try:
        toml_data = open(filename).read()
        data = toml.loads(toml_data)
    except FileNotFoundError:
        print("Wrong file or file path (or) Config file does not exist")
        logging.info("Wrong file or file path (or) Config file does not exist")
    return data
    
######################## Getting the tags present in Risksense #########################################


def get_tags(url,key,client,tag_prefix,tag_owner_id):
   
    tag_url = url+"/api/v1/client/"+ str(client) + "/tag/search"
    payload = json.dumps({"filters":[],"projection":"internal","sort":[{"field":"UPDATED","direction":"DESC"}],"page":0,"size":1000})
    headers = {
      'x-api-key': key,
      'Content-Type': 'application/json'
    }

    print("Getting All tags present in Risksense...\n")    
    try:
        response = requests.request("POST", tag_url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        logging.error(e)

    get_tag_names = response.json()
    
    get_tag_data_RS = []
    tag_name_list = []
    tag_id_list = []
    
    for i in range(len(get_tag_names["_embedded"]["tags"])):
        for j in range(len(get_tag_names["_embedded"]["tags"][i]["tag"])):
            if(str(get_tag_names["_embedded"]["tags"][i]["tag"][j]["uid"] == "NAME" ) and str(get_tag_names["_embedded"]["tags"][i]["tag"][j]["value"])).startswith(tag_prefix): 
                
                tag_id = get_tag_names["_embedded"]["tags"][i]["id"]
                tag_name = get_tag_names["_embedded"]["tags"][i]["tag"][j]["value"]
                
                # Calling edit endpoint for tags
                
                edit_url = url + "/api/v1/client/"+ str(client) + "/admin/tag/" + str(tag_id)
                
                json_data = json.dumps({ 'fields': [ { 'uid': 'TAG_TYPE', 'value': 'CUSTOM', }, { 'uid': 'NAME', 'value': tag_name , }, { 'uid': 'DESCRIPTION', 'value': 'Neurons Tag', }, { 'uid': 'OWNER', 'value': tag_owner_id, }, { 'uid': 'COLOR', 'value': '#648d9f', }, { 'uid': 'LOCKED', 'value': False, }, { 'uid': 'PROPAGATE_TO_ALL_FINDINGS', 'value': True, }, ], })
                
                print("Making an edit on tag {0} for the findings to appear...\n".format(tag_name))
                
                response = requests.request("PUT", edit_url, headers=headers, data=json_data)
                
                
    print("Fetching the updated tags...\n")
    try:
        response = requests.request("POST", tag_url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        logging.error(e) 
    get_tag_names = response.json() 

    
    for i in range(len(get_tag_names["_embedded"]["tags"])):
        for j in range(len(get_tag_names["_embedded"]["tags"][i]["tag"])):
            if(str(get_tag_names["_embedded"]["tags"][i]["tag"][j]["uid"] == "NAME" ) and str(get_tag_names["_embedded"]["tags"][i]["tag"][j]["value"])).startswith(tag_prefix):         
                    tag_name_list.append(get_tag_names["_embedded"]["tags"][i]["tag"][j]["value"])
                    get_tag_data_RS.append(get_tag_names["_embedded"]["tags"][i]["tag"])
                    tag_id_list.append(get_tag_names["_embedded"]["tags"][i]["id"])  
                    
                
    return tag_name_list,tag_id_list,get_tag_data_RS  
        

################################## Export findings using tag ##########################################

def export_findings_create_ticket(platform, key, client, file_name,tag_name_list,tag_id_list,get_tag_data_RS,ism_url,ism_key,ism_attachment_url,post_tag,assignee_prefix,default_assignee,profile_link,tag_owner_id,rs_tag_prefix):
    
    success = False
    flag_AH = ''
    status = ''
    
    for i in range(len(tag_name_list)):
        
######################################## Determining the type of findings in each tag #####################################

        if (assignee_prefix in tag_name_list[i]):
            assignee= tag_name_list[i].split(assignee_prefix)[1]
            assignee_desc = "\nThe Findings are routed to the assignee : {0}".format(assignee)
            assignee = assignee[0:2].upper() + assignee[2:].lower()
        else: 
            assignee = default_assignee
            assignee_desc = "\nThe Findings are routed to default assignee : {0}".format(assignee)
            assignee = assignee[0:2].upper() + assignee[2:].lower()
        #print("Assigning to", assignee)

        flag_AH = ''
        #print(flag_AH,i,get_tag_data_RS[i])
        for l in range(len(get_tag_data_RS[i])):
            if(flag_AH == "A" or flag_AH =="H"):
                    break
            for m in range(len(get_tag_data_RS[i])):    
                
                if(str(get_tag_data_RS[i][m]["uid"]) == "APPLICATION_FINDING_COUNT" and str(get_tag_data_RS[i][m]["value"]) != "0" ):
                    url = platform + "/api/v1/client/" + str(client) + "/applicationFinding/export"
                    flag_AH = "A"
                    
                    payload = json.dumps({"fileName":"sample","fileType":"CSV","noOfRows":"5000","filterRequest":{ "filters": [ { "field": "tags", "exclusive": False, "operator": "IN", "orWithPrevious": False, "implicitFilters": [], "value": tag_name_list[i] } ], "projection": "internal", "sort": [ { "field": "riskRating", "direction": "DESC" } ], "page": 0, "size": 50 },"exportableFields":[{"heading":"asset_options","fields":[{"identifierField":"location","displayText":"Address","sortable":False,"fieldOrder":1,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"addressType","displayText":"Address Type","sortable":False,"fieldOrder":2,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetCriticality","displayText":"Asset Criticality","sortable":False,"fieldOrder":3,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"asset_owner","displayText":"Asset Owner","sortable":False,"fieldOrder":4,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"critical","displayText":"Critical","sortable":False,"fieldOrder":5,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"discoveredOn","displayText":"Discovered On","sortable":False,"fieldOrder":6,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"exploit","displayText":"Exploit","sortable":False,"fieldOrder":7,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifiedBy","displayText":"First Asset Identified By","sortable":False,"fieldOrder":8,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifier","displayText":"First Asset Identifier","sortable":False,"fieldOrder":9,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerFirstDiscoveredOn","displayText":"First Discovered On","sortable":False,"fieldOrder":10,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformFirstIngestedOn","displayText":"First Ingested On","sortable":False,"fieldOrder":11,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupIds","displayText":"Group Ids","sortable":False,"fieldOrder":12,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupNames","displayText":"Group Names","sortable":False,"fieldOrder":13,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"high","displayText":"High","sortable":False,"fieldOrder":14,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"id","displayText":"Id","sortable":False,"fieldOrder":15,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"info","displayText":"Info","sortable":False,"fieldOrder":16,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifiedBy","displayText":"Last Asset Identified By","sortable":False,"fieldOrder":17,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifier","displayText":"Last Asset Identifier","sortable":False,"fieldOrder":18,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerLastDiscoveredOn","displayText":"Last Discovered On","sortable":False,"fieldOrder":19,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastFoundOn","displayText":"Last Found On","sortable":False,"fieldOrder":20,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformLastIngestedOn","displayText":"Last Ingested On","sortable":False,"fieldOrder":21,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"locationCount","displayText":"Location Count","sortable":False,"fieldOrder":22,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"low","displayText":"Low","sortable":False,"fieldOrder":23,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"medium","displayText":"Medium","sortable":False,"fieldOrder":24,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideDate","displayText":"Metric Exclude Override Date","sortable":False,"fieldOrder":25,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideType","displayText":"Metric Exclude Override Status","sortable":False,"fieldOrder":26,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideUser","displayText":"Metric Exclude Override User","sortable":False,"fieldOrder":27,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"name","displayText":"Name","sortable":False,"fieldOrder":28,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"network","displayText":"Network","sortable":False,"fieldOrder":29,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"networkType","displayText":"Network Type","sortable":False,"fieldOrder":30,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"osName","displayText":"OS Name","sortable":False,"fieldOrder":31,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"pii","displayText":"PII","sortable":False,"fieldOrder":32,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"rs3","displayText":"RS3","sortable":False,"fieldOrder":33,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"sla_rule_name","displayText":"SLA Name","sortable":False,"fieldOrder":34,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tags","displayText":"Tags","sortable":False,"fieldOrder":35,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsId","displayText":"Tickets Id","sortable":False,"fieldOrder":36,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsLink","displayText":"Tickets Link","sortable":False,"fieldOrder":37,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsStatus","displayText":"Tickets Status","sortable":False,"fieldOrder":38,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrCritical","displayText":"VRR Critical","sortable":False,"fieldOrder":39,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrHigh","displayText":"VRR High","sortable":False,"fieldOrder":40,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrInfo","displayText":"VRR Info","sortable":False,"fieldOrder":41,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrLow","displayText":"VRR Low","sortable":False,"fieldOrder":42,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrMedium","displayText":"VRR Medium","sortable":False,"fieldOrder":43,"selected":True,"sortOrder":0,"sortType":"ASC"}]},{"heading":"finding_options","fields":[{"identifierField":"addressType","displayText":"Address Type","sortable":False,"fieldOrder":1,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"appId","displayText":"App Id","sortable":False,"fieldOrder":2,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"name","displayText":"App Name","sortable":False,"fieldOrder":3,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"applicationAddress","displayText":"Application Address","sortable":False,"fieldOrder":4,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetCriticality","displayText":"Asset Criticality","sortable":False,"fieldOrder":5,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"asset_owner","displayText":"Asset Owner","sortable":False,"fieldOrder":6,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assignedTo","displayText":"Assigned To","sortable":False,"fieldOrder":7,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss2Score","displayText":"CVSS 2.0","sortable":False,"fieldOrder":8,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss2Vector","displayText":"CVSS 2.0 Vector","sortable":False,"fieldOrder":9,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss3Score","displayText":"CVSS 3.0","sortable":False,"fieldOrder":10,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss3Vector","displayText":"CVSS 3.0 Vector","sortable":False,"fieldOrder":11,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"description","displayText":"Description","sortable":False,"fieldOrder":12,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"discoveredOn","displayText":"Discovered On","sortable":False,"fieldOrder":13,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"dueDate","displayText":"Due Date","sortable":False,"fieldOrder":14,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"expireDate","displayText":"Expire Date","sortable":False,"fieldOrder":15,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"exploits","displayText":"Exploits","sortable":False,"fieldOrder":16,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifiedBy","displayText":"First Asset Identified By","sortable":False,"fieldOrder":17,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifier","displayText":"First Asset Identifier","sortable":False,"fieldOrder":18,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerFirstDiscoveredOn","displayText":"First Discovered On","sortable":False,"fieldOrder":19,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformFirstIngestedOn","displayText":"First Ingested On","sortable":False,"fieldOrder":20,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupIds","displayText":"Group Ids","sortable":False,"fieldOrder":21,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupNames","displayText":"Group Names","sortable":False,"fieldOrder":22,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"id","displayText":"Id","sortable":False,"fieldOrder":23,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifiedBy","displayText":"Last Asset Identified By","sortable":False,"fieldOrder":24,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifier","displayText":"Last Asset Identifier","sortable":False,"fieldOrder":25,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerLastDiscoveredOn","displayText":"Last Discovered On","sortable":False,"fieldOrder":26,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastFoundOn","displayText":"Last Found On","sortable":False,"fieldOrder":27,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformLastIngestedOn","displayText":"Last Ingested On","sortable":False,"fieldOrder":28,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"location","displayText":"Location","sortable":False,"fieldOrder":29,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"network","displayText":"Network","sortable":False,"fieldOrder":30,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"networkType","displayText":"Network Type","sortable":False,"fieldOrder":31,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"notes","displayText":"Notes","sortable":False,"fieldOrder":32,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"originalAggregatedSeverity","displayText":"Original Aggregated Severity","sortable":False,"fieldOrder":33,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"osName","displayText":"OS Name","sortable":False,"fieldOrder":34,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"parameter","displayText":"Parameter","sortable":False,"fieldOrder":35,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"patchId","displayText":"Patch Id","sortable":False,"fieldOrder":36,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"payload","displayText":"Payload","sortable":False,"fieldOrder":37,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"possiblePatches","displayText":"Possible Patches","sortable":False,"fieldOrder":38,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"solution","displayText":"Possible Solution","sortable":False,"fieldOrder":39,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ransomwareFamily","displayText":"Ransomware Family","sortable":False,"fieldOrder":40,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"resolvedOn","displayText":"Resolved On","sortable":False,"fieldOrder":41,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"resourceCpe","displayText":"Resource CPE","sortable":False,"fieldOrder":42,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerName","displayText":"Scanner Name","sortable":False,"fieldOrder":43,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerOutput","displayText":"Scanner Output","sortable":False,"fieldOrder":44,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerPlugin","displayText":"Scanner Plugin","sortable":False,"fieldOrder":45,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerReportedSeverity","displayText":"Scanner Reported Severity","sortable":False,"fieldOrder":46,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severity","displayText":"Severity","sortable":False,"fieldOrder":47,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severityGroup","displayText":"Severity Group","sortable":False,"fieldOrder":48,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severityOverride","displayText":"Severity Override","sortable":False,"fieldOrder":49,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"status","displayText":"Status","sortable":False,"fieldOrder":50,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tags","displayText":"Tags","sortable":False,"fieldOrder":51,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsId","displayText":"Tickets Id","sortable":False,"fieldOrder":52,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsLink","displayText":"Tickets Link","sortable":False,"fieldOrder":53,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsStatus","displayText":"Tickets Status","sortable":False,"fieldOrder":54,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrGroup","displayText":"VRR Group","sortable":False,"fieldOrder":55,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vulnerability","displayText":"Vulnerability","sortable":False,"fieldOrder":56,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vulnerabilityRiskRating","displayText":"Vulnerability Risk Rating","sortable":False,"fieldOrder":57,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchCreated","displayText":"Workflow Create Date","sortable":False,"fieldOrder":58,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchCreatedBy","displayText":"Workflow Created By","sortable":False,"fieldOrder":59,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchExpiration","displayText":"Workflow Expiration Date","sortable":False,"fieldOrder":60,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchId","displayText":"Workflow Id","sortable":False,"fieldOrder":61,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchReason","displayText":"Workflow Reason","sortable":False,"fieldOrder":62,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchState","displayText":"Workflow State","sortable":False,"fieldOrder":63,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchUserNote","displayText":"Workflow State User Note","sortable":False,"fieldOrder":64,"selected":False,"sortOrder":0,"sortType":"ASC"}]}]})
                    break
    
                elif(str(get_tag_data_RS[i][m]["uid"]) == "HOST_FINDING_COUNT" and str(get_tag_data_RS[i][m]["value"]) != "0" ):
                    url = platform + "/api/v1/client/" + str(client) + "/hostFinding/export"
                    flag_AH = "H"
                    
                    payload = json.dumps({"fileName":"sample","fileType":"CSV","noOfRows":"5000","filterRequest":{ "filters": [ { "field": "tags", "exclusive": False, "operator": "IN", "orWithPrevious": False, "implicitFilters": [], "value": tag_name_list[i] } ], "projection": "internal", "sort": [ { "field": "riskRating", "direction": "DESC" } ], "page": 0, "size": 50 },"exportableFields":[{"heading":"asset_options","fields":[{"identifierField":"addressType","displayText":"Address Type","sortable":False,"fieldOrder":1,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"criticality","displayText":"Asset Criticality","sortable":False,"fieldOrder":2,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tags","displayText":"Asset Tags","sortable":False,"fieldOrder":3,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbAssetCriticality","displayText":"CMDB Asset Criticality","sortable":False,"fieldOrder":4,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbAssetTags","displayText":"CMDB Asset Tags","sortable":False,"fieldOrder":5,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField1","displayText":"CMDB Custom Field 1","sortable":False,"fieldOrder":6,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField10","displayText":"CMDB Custom Field 10","sortable":False,"fieldOrder":7,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField2","displayText":"CMDB Custom Field 2","sortable":False,"fieldOrder":8,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField3","displayText":"CMDB Custom Field 3","sortable":False,"fieldOrder":9,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField4","displayText":"CMDB Custom Field 4","sortable":False,"fieldOrder":10,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField5","displayText":"CMDB Custom Field 5","sortable":False,"fieldOrder":11,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField6","displayText":"CMDB Custom Field 6","sortable":False,"fieldOrder":12,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField7","displayText":"CMDB Custom Field 7","sortable":False,"fieldOrder":13,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField8","displayText":"CMDB Custom Field 8","sortable":False,"fieldOrder":14,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbCustomField9","displayText":"CMDB Custom Field 9","sortable":False,"fieldOrder":15,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbFERPAComplianceAsset","displayText":"CMDB FERPA Compliance Asset","sortable":False,"fieldOrder":16,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbHIPAAComplianceAsset","displayText":"CMDB HIPAA Compliance Asset","sortable":False,"fieldOrder":17,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbLastScanned","displayText":"CMDB Last Scanned","sortable":False,"fieldOrder":18,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbLocation","displayText":"CMDB Location","sortable":False,"fieldOrder":19,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbMacAddress","displayText":"CMDB Mac Address","sortable":False,"fieldOrder":20,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbManagedBy","displayText":"CMDB Managed By","sortable":False,"fieldOrder":21,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbManufacturedBy","displayText":"CMDB Manufactured By","sortable":False,"fieldOrder":22,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbModel","displayText":"CMDB Model","sortable":False,"fieldOrder":23,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbOperatingSystem","displayText":"CMDB Operating System","sortable":False,"fieldOrder":24,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbOwnedBy","displayText":"CMDB Owned By","sortable":False,"fieldOrder":25,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbPCIComplianceAsset","displayText":"CMDB PCI Compliance Asset","sortable":False,"fieldOrder":26,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbSupportGroup","displayText":"CMDB Support Group","sortable":False,"fieldOrder":27,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cmdbSupportedBy","displayText":"CMDB Supported By","sortable":False,"fieldOrder":28,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"critical","displayText":"Critical","sortable":False,"fieldOrder":29,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"discoveredOn","displayText":"Discovered On","sortable":False,"fieldOrder":30,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"dns","displayText":"DNS","sortable":False,"fieldOrder":31,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ec2Identifier","displayText":"EC2 identifier","sortable":False,"fieldOrder":32,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"expanse_asset_identifier","displayText":"Expanse Asset Identifier","sortable":False,"fieldOrder":33,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"exploit","displayText":"Exploit","sortable":False,"fieldOrder":34,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"agent_id","displayText":"FalconSpotlight Agent ID","sortable":False,"fieldOrder":35,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"findingsCount","displayText":"Finding Count","sortable":False,"fieldOrder":36,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifiedBy","displayText":"First Asset Identified By","sortable":False,"fieldOrder":37,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifier","displayText":"First Asset Identifier","sortable":False,"fieldOrder":38,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerFirstDiscoveredOn","displayText":"First Discovered On","sortable":False,"fieldOrder":39,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformFirstIngestedOn","displayText":"First Ingested On","sortable":False,"fieldOrder":40,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"fqdn","displayText":"FQDN","sortable":False,"fieldOrder":41,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupIds","displayText":"Group Ids","sortable":False,"fieldOrder":42,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupNames","displayText":"Group Names","sortable":False,"fieldOrder":43,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"high","displayText":"High","sortable":False,"fieldOrder":44,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"hostId","displayText":"Id","sortable":False,"fieldOrder":45,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"info","displayText":"Info","sortable":False,"fieldOrder":46,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ipAddress","displayText":"IP Address","sortable":False,"fieldOrder":47,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"easilyExploitable","displayText":"Is Easily Exploitable","sortable":False,"fieldOrder":48,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifiedBy","displayText":"Last Asset Identified By","sortable":False,"fieldOrder":49,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifier","displayText":"Last Asset Identifier","sortable":False,"fieldOrder":50,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastCredentialedScanDate","displayText":"Last Credentialed Scan","sortable":False,"fieldOrder":51,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerLastDiscoveredOn","displayText":"Last Discovered On","sortable":False,"fieldOrder":52,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastFoundOn","displayText":"Last Found On","sortable":False,"fieldOrder":53,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformLastIngestedOn","displayText":"Last Ingested On","sortable":False,"fieldOrder":54,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"low","displayText":"Low","sortable":False,"fieldOrder":55,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"macAddress","displayText":"MAC address","sortable":False,"fieldOrder":56,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"medium","displayText":"Medium","sortable":False,"fieldOrder":57,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideDate","displayText":"Metric Exclude Override Date","sortable":False,"fieldOrder":58,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideType","displayText":"Metric Exclude Override Status","sortable":False,"fieldOrder":59,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"metricsOverrideUser","displayText":"Metric Exclude Override User","sortable":False,"fieldOrder":60,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"hostname","displayText":"Name","sortable":False,"fieldOrder":61,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"netbios","displayText":"NetBIOS","sortable":False,"fieldOrder":62,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"network","displayText":"Network","sortable":False,"fieldOrder":63,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"networkType","displayText":"Network Type","sortable":False,"fieldOrder":64,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"device_id","displayText":"Nexpose Device ID","sortable":False,"fieldOrder":65,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"osName","displayText":"OS Name","sortable":False,"fieldOrder":66,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ports","displayText":"Ports","sortable":False,"fieldOrder":67,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"QG_HOSTID","displayText":"Qualys Host ID","sortable":False,"fieldOrder":68,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"rs3","displayText":"RS3","sortable":False,"fieldOrder":69,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"services","displayText":"Services","sortable":False,"fieldOrder":70,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"sla_rule_name","displayText":"SLA Name","sortable":False,"fieldOrder":71,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"host_uuid","displayText":"Tenable Host UUID","sortable":False,"fieldOrder":72,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tenable_uuid","displayText":"Tenable UUID","sortable":False,"fieldOrder":73,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsId","displayText":"Tickets Id","sortable":False,"fieldOrder":74,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsLink","displayText":"Tickets Link","sortable":False,"fieldOrder":75,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsStatus","displayText":"Tickets Status","sortable":False,"fieldOrder":76,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrCritical","displayText":"VRR Critical","sortable":False,"fieldOrder":77,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrHigh","displayText":"VRR High","sortable":False,"fieldOrder":78,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrInfo","displayText":"VRR Info","sortable":False,"fieldOrder":79,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrLow","displayText":"VRR Low","sortable":False,"fieldOrder":80,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrMedium","displayText":"VRR Medium","sortable":False,"fieldOrder":81,"selected":False,"sortOrder":0,"sortType":"ASC"}]},{"heading":"finding_options","fields":[{"identifierField":"criticality","displayText":"Asset Criticality","sortable":False,"fieldOrder":1,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assignedTo","displayText":"Assigned To","sortable":False,"fieldOrder":2,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cves","displayText":"CVEs Associated","sortable":False,"fieldOrder":3,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss2Score","displayText":"CVSS 2.0","sortable":False,"fieldOrder":4,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss2Vector","displayText":"CVSS 2.0 Vector","sortable":False,"fieldOrder":5,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss3Score","displayText":"CVSS 3.0","sortable":False,"fieldOrder":6,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"cvss3Vector","displayText":"CVSS 3.0 Vector","sortable":False,"fieldOrder":7,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"discoveredOn","displayText":"Discovered On","sortable":False,"fieldOrder":8,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"dns","displayText":"DNS","sortable":False,"fieldOrder":9,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"dueDate","displayText":"Due Date","sortable":False,"fieldOrder":10,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ec2Identifier","displayText":"EC2 identifier","sortable":False,"fieldOrder":11,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"expanse_asset_identifier","displayText":"Expanse Asset Identifier","sortable":False,"fieldOrder":12,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"expireDate","displayText":"Expire Date","sortable":False,"fieldOrder":13,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"exploits","displayText":"Exploits","sortable":False,"fieldOrder":14,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"agent_id","displayText":"FalconSpotlight Agent ID","sortable":False,"fieldOrder":15,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"findingType","displayText":"Finding Type","sortable":False,"fieldOrder":16,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifiedBy","displayText":"First Asset Identified By","sortable":False,"fieldOrder":17,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"assetIdentifier","displayText":"First Asset Identifier","sortable":False,"fieldOrder":18,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerFirstDiscoveredOn","displayText":"First Discovered On","sortable":False,"fieldOrder":19,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformFirstIngestedOn","displayText":"First Ingested On","sortable":False,"fieldOrder":20,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"fqdn","displayText":"FQDN","sortable":False,"fieldOrder":21,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupIds","displayText":"Group Ids","sortable":False,"fieldOrder":22,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"groupNames","displayText":"Group Names","sortable":False,"fieldOrder":23,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"defaultCredentials","displayText":"Has Default Credentials","sortable":False,"fieldOrder":24,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"hasTicket","displayText":"Has Ticket","sortable":False,"fieldOrder":25,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"hostId","displayText":"Host Id","sortable":False,"fieldOrder":26,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"host","displayText":"Host Name","sortable":False,"fieldOrder":27,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"id","displayText":"Id","sortable":False,"fieldOrder":28,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ipAddress","displayText":"IP Address","sortable":False,"fieldOrder":29,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifiedBy","displayText":"Last Asset Identified By","sortable":False,"fieldOrder":30,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastAssetIdentifier","displayText":"Last Asset Identifier","sortable":False,"fieldOrder":31,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerLastDiscoveredOn","displayText":"Last Discovered On","sortable":False,"fieldOrder":32,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"lastFoundOn","displayText":"Last Found On","sortable":False,"fieldOrder":33,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"platformLastIngestedOn","displayText":"Last Ingested On","sortable":False,"fieldOrder":34,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"macAddress","displayText":"MAC address","sortable":False,"fieldOrder":35,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"malware","displayText":"Malware","sortable":False,"fieldOrder":36,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"netbios","displayText":"NetBIOS","sortable":False,"fieldOrder":37,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"network","displayText":"Network","sortable":False,"fieldOrder":38,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"networkType","displayText":"Network Type","sortable":False,"fieldOrder":39,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"device_id","displayText":"Nexpose Device ID","sortable":False,"fieldOrder":40,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"notes","displayText":"Notes","sortable":False,"fieldOrder":41,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"originalAggregatedSeverity","displayText":"Original Aggregated Severity","sortable":False,"fieldOrder":42,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"osName","displayText":"OS Name","sortable":False,"fieldOrder":43,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"patchId","displayText":"Patch Id","sortable":False,"fieldOrder":44,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"patchTitle","displayText":"Patch Title","sortable":False,"fieldOrder":45,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"pluginCpes","displayText":"Plugin CPE","sortable":False,"fieldOrder":46,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"port","displayText":"Port","sortable":False,"fieldOrder":47,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"possiblePatches","displayText":"Possible Patches","sortable":False,"fieldOrder":48,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"possibleSolution","displayText":"Possible Solution","sortable":False,"fieldOrder":49,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"QG_HOSTID","displayText":"Qualys Host ID","sortable":False,"fieldOrder":50,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ransomwareFamily","displayText":"Ransomware Family","sortable":False,"fieldOrder":51,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"resolvedOn","displayText":"Resolved On","sortable":False,"fieldOrder":52,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scanDate","displayText":"Scan Date","sortable":False,"fieldOrder":53,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerName","displayText":"Scanner Name","sortable":False,"fieldOrder":54,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerOutput","displayText":"Scanner Output","sortable":False,"fieldOrder":55,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerPluginId","displayText":"Scanner Plugin ID","sortable":False,"fieldOrder":56,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"scannerReportedSeverity","displayText":"Scanner Reported Severity","sortable":False,"fieldOrder":57,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"service","displayText":"Service","sortable":False,"fieldOrder":58,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severity","displayText":"Severity","sortable":False,"fieldOrder":59,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severityGroup","displayText":"Severity Group","sortable":False,"fieldOrder":60,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"severityOverride","displayText":"Severity Override","sortable":False,"fieldOrder":61,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"status","displayText":"Status","sortable":False,"fieldOrder":62,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tags","displayText":"Tags","sortable":False,"fieldOrder":63,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"host_uuid","displayText":"Tenable Host UUID","sortable":False,"fieldOrder":64,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"tenable_uuid","displayText":"Tenable UUID","sortable":False,"fieldOrder":65,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"testStatus","displayText":"Test Status","sortable":False,"fieldOrder":66,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsId","displayText":"Tickets Id","sortable":False,"fieldOrder":67,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsLink","displayText":"Tickets Link","sortable":False,"fieldOrder":68,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"ticketsStatus","displayText":"Tickets Status","sortable":False,"fieldOrder":69,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vrrGroup","displayText":"VRR Group","sortable":False,"fieldOrder":70,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vulnerability","displayText":"Vulnerability","sortable":False,"fieldOrder":71,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"riskRating","displayText":"Vulnerability Risk Rating","sortable":False,"fieldOrder":72,"selected":True,"sortOrder":0,"sortType":"ASC"},{"identifierField":"vulnerabilityType","displayText":"Vulnerability Type","sortable":False,"fieldOrder":73,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchCreated","displayText":"Workflow Create Date","sortable":False,"fieldOrder":74,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchCreatedBy","displayText":"Workflow Created By","sortable":False,"fieldOrder":75,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchExpiration","displayText":"Workflow Expiration Date","sortable":False,"fieldOrder":76,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchId","displayText":"Workflow Id","sortable":False,"fieldOrder":77,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchReason","displayText":"Workflow Reason","sortable":False,"fieldOrder":78,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchState","displayText":"Workflow State","sortable":False,"fieldOrder":79,"selected":False,"sortOrder":0,"sortType":"ASC"},{"identifierField":"workflowBatchUserNote","displayText":"Workflow State User Note","sortable":False,"fieldOrder":80,"selected":False,"sortOrder":0,"sortType":"ASC"}]}]})
                    break
   
        print("Exporting the findings associated with the tag "+ tag_name_list[i])
        logging.info("Exporting the findings associated with the tag "+ tag_name_list[i])
        print(url,flag_AH)
        
        headers = {
      'x-api-key': key,
      'Content-Type': 'application/json'
    }
            
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
        except Exception as e:
            print(e)
            logging.error(e)
        response = requests.request("POST", url, headers=headers, data=payload)

        if response and response.status_code == 200:
            print("Export request submitted successfully.")
            logging.info("Export request submitted successfully.")
            jsonified_response = json.loads(response.text)
            export_identifier = jsonified_response['id']

        # If not successful...
        else:
            print("There was an error requesting your export.")
            logging.error("There was an error requesting your export.")
            print(f"Response Status Code: {response.status_code}")
            logging.error(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            logging.error(f"Response Text: {response.text}")
            exit(1)

        
################################### Download exported file ############################################

        success = False
        print()
        print("Downloading the file with the findings...")
        logging.info("Downloading the file with the findings...")
        print()

        url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export_identifier)

        print("Attempting to download your export file.")
        logging.info("Attempting to download your export file.")
        
        time.sleep(30)
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            logging.error(e)

        if response.status_code == 200:
            print("\nWriting your file to disk.\n")
            logging.info("\nWriting your file to disk.\n")
            open(file_name, "wb").write(response.content)
            print(" - Done.")
            logging.info(" - Done.")
            
            success = True

        else:
            print("There was an error getting your file.")
            logging.error("There was an error getting your file.")
            print(f"Response Status Code: {response.status_code}")
            logging.error(f"Response Status Code: {response.status_code}")
            print(f"Response Text:{response.text}")
            logging.error(f"Response Text:{response.text}")
            
            exit(1)
        
        
        wait_time = 30  # Seconds
        counter = 0

        while counter < wait_time:
            if counter == 0:
                print(f" - Sleeping for {wait_time - counter} seconds to allow the platform some time to generate the file.")
                logging.info(f" - Sleeping for {wait_time - counter} seconds to allow the platform some time to generate the file.")
            time.sleep(1)
            counter += 1
        # Request download from the platform.
        
        export_folder = str(date.today()) + "_" +  str(time_today)
        if success:
            print("Success.")
            logging.info("Success.")
            
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()
            os.remove(file_name)
            
            ts = date.today()
            ts = str(ts).replace(' ','')
            folder = export_folder
            current_directory = os.getcwd()
            
            final_directory = os.path.join(current_directory, folder)
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)
            
            os.replace("Assets.csv", final_directory+"/Assets_"+str(tag_name_list[i])+".csv")
            os.replace("Findings.csv", final_directory+"/Findings_"+str(tag_name_list[i])+".csv")

            df = pd.read_csv(final_directory+"/Findings_"+str(tag_name_list[i])+".csv")
            df = df.drop_duplicates()
            #print(df)
            df.to_csv(final_directory+"/Ticket_Findings_"+str(tag_name_list[i])+".csv")
          
        else:
            print("There was an error downloading your export file from the platform.")
            logging.error("There was an error downloading your export file from the platform.")
            exit(1)
           
                
####################################################### Incident creation part ###################################################################    

        print()
        print("Creating an incident in ISM...")
        logging.info("Creating an incident in ISM...")
        print()
        Incident_num = ISM.incident_create(ism_url,ism_key,ism_attachment_url,final_directory,tag_name_list[i],flag_AH,assignee,assignee_desc,profile_link)
        
        status,text = change_tag_name(platform,key,client,tag_id_list[i],Incident_num,post_tag,tag_owner_id)
        print()
        if(status == 200 ):
            print("Change tag is done...Now , you have the tag {0} is renamed to ISM incident {1} in Risksense platform...\n".format(tag_name_list[i],Incident_num))
            logging.info("Change tag is done...Now , you have the tag {0} is renamed to ISM incident {1} in Risksense platform...\n".format(tag_name_list[i],Incident_num))
            print("==========================================================================================================\n")
            logging.info("==========================================================================================================\n")
        else:
            print(text)    
            logging.error(text)
        #print("Sleeping for 30 seconds...")
        #time.sleep(30)
    return status        
            
def change_tag_name(url,key,client,tag_id_list,incident_num,post_tag,tag_owner_id):

    url = url+"/api/v1/client/"+ str(client) + "/admin/tag/"+ str(tag_id_list)
    
    headers = {
    'accept': 'application/json',
    'x-api-key': key,
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    }
    json_data = { 'fields': [ { 'uid': 'TAG_TYPE', 'value': 'CUSTOM', }, { 'uid': 'NAME', 'value': post_tag+ str(incident_num) , }, { 'uid': 'DESCRIPTION', 'value': 'Neurons Tag', }, { 'uid': 'OWNER', 'value': tag_owner_id, }, { 'uid': 'COLOR', 'value': '#648d9f', }, { 'uid': 'LOCKED', 'value': False, }, { 'uid': 'PROPAGATE_TO_ALL_FINDINGS', 'value': True, }, ], }
    try:
        response = requests.put(url, headers=headers, json=json_data)
    except Exception as e:
        print(e)
        logging.error(e)

    return response.status_code,response.text

    
######################################### Main #############################################

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    args = parser.parse_args()      
    
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'Incident_creation.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)    
    logging.basicConfig(filename=log_file, level=args.loglevel,format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    print("**** STARTING THE Incident Creation SCRIPT ****\n")
    logging.info("**** STARTING THE Incident Creation SCRIPT ****\n")

    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    configuration = read_config_file(conf_file)
    #tag_name = configuration["platform"]["tag_name"] 
    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']
    file_name = configuration['platform']['file_name']
    ism_attachment_url = configuration['ISM']['ism_attachment_url']
    ism_url = configuration['ISM']['ism_url']
    ism_key = configuration['ISM']['ism_key']
    rs_tag_prefix = configuration['platform']['tag_prefix']
    post_tag = configuration['platform']['incident_prefix']
    assignee_prefix = configuration['ISM']['assignee_prefix']
    default_assignee = configuration['ISM']['default_assignee']
    profile_link = configuration['ISM']['profile_link']
    tag_owner_id = configuration['platform']['tag_owner']

    tag_name_list,tag_id_list,get_tag_names = get_tags(rs_url,api_key,client_id,rs_tag_prefix,tag_owner_id)
    if not tag_name_list:
        print("No tags present")
        logging.info("No tags present")
        exit(0)
    #print(tag_name_list)
    file_name = file_name + '.zip'
    status = export_findings_create_ticket(rs_url, api_key, client_id,file_name ,tag_name_list,tag_id_list,get_tag_names,ism_url,ism_key,ism_attachment_url,post_tag,assignee_prefix,default_assignee,profile_link,tag_owner_id,rs_tag_prefix)
    if(status == 200):
        path = os.path.join(os.getcwd(), str(date.today()) + "_" +  str(time_today))
        shutil.rmtree(path, ignore_errors=False, onerror=None)
    else:
        shutil.rmtree(path, ignore_errors=False, onerror=None)
    
    
if __name__ == "__main__":
    main()
