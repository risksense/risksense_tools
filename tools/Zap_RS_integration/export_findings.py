"""********************************************************************************************************************
|
|  Name        :  export_hostfindings.py
|  Description :  Exports and downloads a csv file containing hostfindings from the RiskSense platform via the REST API.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0
|
********************************************************************************************************************"""

import json
import time
import os
import requests
import toml
import zipfile
from datetime import date
import sys
import argparse
import logging

def initiate_export(platform, key, client, filename,assessment_name):

    """
    Initiates the generation of an export file containing all host findings in .csv format.

    :param platform:    URL of RiskSense Platform to be queried
    :type  platform:    str

    :param key:         API Key.
    :type  key:         str

    :param client:      Client ID associated with data to be exported.
    :type  client:      int

    :param filename:    Specifies the desired filename for the export.
    :type  filename:    str

    :return:    Returns the identifier for the export.
    :rtype:     int
    """

    print()
    print("The data is being exported for the assessment: ",assessment_name)
    print("Submitting request for host finding file export.")
    export_identifier = 0
    #todays_date = datetime.date.today()

    #  Assemble the URL for the API call
    #  https://<platform>/api/vi/client/<client ID>/hostFinding/export
    api_url = platform + '/api/v1/client/' + str(client) + '/applicationFinding/export'

    #  Define the header for the API call
    header = {
        "x-api-key": key,
        "content-type": "application/json",
        "Cache-Control": "no-cache"
    }

    #  This is where we define the filter(s) to be sed when generating the requested
    #  export file.  In this case, we are filtering for host findings that have
    #  threats.

    
  

    #  Define the body for the API call.
    body = { "fileName": "exportsample", "fileType": "CSV", "noOfRows": "5000", "filterRequest": { "filters": [ { "field": "assessment_labels", "exclusive": False, "operator": "IN", "orWithPrevious": False, "implicitFilters": [], "value": assessment_name } ] }, "exportableFields": [ { "heading": "asset_options", "fields": [ { "identifierField": "location", "displayText": "Address", "sortable": False, "fieldOrder": 1, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "addressType", "displayText": "Address Type", "sortable": False, "fieldOrder": 2, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assetCriticality", "displayText": "Asset Criticality", "sortable": False, "fieldOrder": 3, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "critical", "displayText": "Critical", "sortable": False, "fieldOrder": 5, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "discoveredOn", "displayText": "Discovered On", "sortable": False, "fieldOrder": 6, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "exploit", "displayText": "Exploit", "sortable": False, "fieldOrder": 7, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assetIdentifier", "displayText": "First Asset Identifier", "sortable": False, "fieldOrder": 9, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "platformFirstIngestedOn", "displayText": "First Ingested On", "sortable": False, "fieldOrder": 11, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "high", "displayText": "High", "sortable": False, "fieldOrder": 14, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "id", "displayText": "Id", "sortable": False, "fieldOrder": 15, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "info", "displayText": "Info", "sortable": False, "fieldOrder": 16, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "lastAssetIdentifiedBy", "displayText": "Last Asset Identified By", "sortable": False, "fieldOrder": 17, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "lastFoundOn", "displayText": "Last Found On", "sortable": False, "fieldOrder": 20, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "osName", "displayText": "OS Name", "sortable": False, "fieldOrder": 31, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "rs3", "displayText": "RS3", "sortable": False, "fieldOrder": 33, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "sla_rule_name", "displayText": "SLA Name", "sortable": False, "fieldOrder": 34, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "tags", "displayText": "Tags", "sortable": False, "fieldOrder": 35, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "ticketsId", "displayText": "Tickets Id", "sortable": False, "fieldOrder": 36, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrCritical", "displayText": "VRR Critical", "sortable": False, "fieldOrder": 39, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrHigh", "displayText": "VRR High", "sortable": False, "fieldOrder": 40, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrInfo", "displayText": "VRR Info", "sortable": False, "fieldOrder": 41, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrLow", "displayText": "VRR Low", "sortable": False, "fieldOrder": 42, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrMedium", "displayText": "VRR Medium", "sortable": False, "fieldOrder": 43, "selected": False, "sortOrder": 0, "sortType": "ASC" } ] }, { "heading": "finding_options", "fields": [ { "identifierField": "addressType", "displayText": "Address Type", "sortable": False, "fieldOrder": 1, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "name", "displayText": "App Name", "sortable": False, "fieldOrder": 3, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "applicationAddress", "displayText": "Application Address", "sortable": False, "fieldOrder": 4, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assetCriticality", "displayText": "Asset Criticality", "sortable": False, "fieldOrder": 5, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "asset_owner", "displayText": "Asset Owner", "sortable": False, "fieldOrder": 6, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assignedTo", "displayText": "Assigned To", "sortable": False, "fieldOrder": 7, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "cvss2Score", "displayText": "CVSS 2.0", "sortable": False, "fieldOrder": 8, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "cvss2Vector", "displayText": "CVSS 2.0 Vector", "sortable": False, "fieldOrder": 9, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "cvss3Score", "displayText": "CVSS 3.0", "sortable": False, "fieldOrder": 10, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "cvss3Vector", "displayText": "CVSS 3.0 Vector", "sortable": False, "fieldOrder": 11, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "description", "displayText": "Description", "sortable": False, "fieldOrder": 12, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "discoveredOn", "displayText": "Discovered On", "sortable": False, "fieldOrder": 13, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "dueDate", "displayText": "Due Date", "sortable": False, "fieldOrder": 14, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "expireDate", "displayText": "Expire Date", "sortable": False, "fieldOrder": 15, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "exploits", "displayText": "Exploits", "sortable": False, "fieldOrder": 16, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assetIdentifiedBy", "displayText": "First Asset Identified By", "sortable": False, "fieldOrder": 17, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "assetIdentifier", "displayText": "First Asset Identifier", "sortable": False, "fieldOrder": 18, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerFirstDiscoveredOn", "displayText": "First Discovered On", "sortable": False, "fieldOrder": 19, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "platformFirstIngestedOn", "displayText": "First Ingested On", "sortable": False, "fieldOrder": 20, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "groupIds", "displayText": "Group Ids", "sortable": False, "fieldOrder": 21, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "groupNames", "displayText": "Group Names", "sortable": False, "fieldOrder": 22, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "id", "displayText": "Id", "sortable": False, "fieldOrder": 23, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "lastAssetIdentifiedBy", "displayText": "Last Asset Identified By", "sortable": False, "fieldOrder": 24, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "lastAssetIdentifier", "displayText": "Last Asset Identifier", "sortable": False, "fieldOrder": 25, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerLastDiscoveredOn", "displayText": "Last Discovered On", "sortable": False, "fieldOrder": 26, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "lastFoundOn", "displayText": "Last Found On", "sortable": False, "fieldOrder": 27, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "platformLastIngestedOn", "displayText": "Last Ingested On", "sortable": False, "fieldOrder": 28, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "location", "displayText": "Location", "sortable": False, "fieldOrder": 29, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "network", "displayText": "Network", "sortable": False, "fieldOrder": 30, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "networkType", "displayText": "Network Type", "sortable": False, "fieldOrder": 31, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "notes", "displayText": "Notes", "sortable": False, "fieldOrder": 32, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "osName", "displayText": "OS Name", "sortable": False, "fieldOrder": 33, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "originalAggregatedSeverity", "displayText": "Original Aggregated Severity", "sortable": False, "fieldOrder": 34, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "parameter", "displayText": "Parameter", "sortable": False, "fieldOrder": 35, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "patchId", "displayText": "Patch Id", "sortable": False, "fieldOrder": 36, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "payload", "displayText": "Payload", "sortable": False, "fieldOrder": 37, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "possiblePatches", "displayText": "Possible Patches", "sortable": False, "fieldOrder": 38, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "solution", "displayText": "Possible Solution", "sortable": False, "fieldOrder": 39, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "ransomwareFamily", "displayText": "Ransomware Family", "sortable": False, "fieldOrder": 40, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "resolvedOn", "displayText": "Resolved On", "sortable": False, "fieldOrder": 41, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "resourceCpe", "displayText": "Resource CPE", "sortable": False, "fieldOrder": 42, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerName", "displayText": "Scanner Name", "sortable": False, "fieldOrder": 43, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerOutput", "displayText": "Scanner Output", "sortable": False, "fieldOrder": 44, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerPlugin", "displayText": "Scanner Plugin", "sortable": False, "fieldOrder": 45, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "scannerReportedSeverity", "displayText": "Scanner Reported Severity", "sortable": False, "fieldOrder": 46, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "severity", "displayText": "Severity", "sortable": False, "fieldOrder": 47, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "severityGroup", "displayText": "Severity Group", "sortable": False, "fieldOrder": 48, "selected": True, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "severityOverride", "displayText": "Severity Override", "sortable": False, "fieldOrder": 49, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "status", "displayText": "Status", "sortable": False, "fieldOrder": 50, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "tags", "displayText": "Tags", "sortable": False, "fieldOrder": 51, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "ticketsId", "displayText": "Tickets Id", "sortable": False, "fieldOrder": 52, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "ticketsLink", "displayText": "Tickets Link", "sortable": False, "fieldOrder": 53, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "ticketsStatus", "displayText": "Tickets Status", "sortable": False, "fieldOrder": 54, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vrrGroup", "displayText": "VRR Group", "sortable": False, "fieldOrder": 55, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vulnerability", "displayText": "Vulnerability", "sortable": False, "fieldOrder": 56, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "vulnerabilityRiskRating", "displayText": "Vulnerability Risk Rating", "sortable": False, "fieldOrder": 57, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchCreated", "displayText": "Workflow Create Date", "sortable": False, "fieldOrder": 58, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchCreatedBy", "displayText": "Workflow Created By", "sortable": False, "fieldOrder": 59, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchExpiration", "displayText": "Workflow Expiration Date", "sortable": False, "fieldOrder": 60, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchId", "displayText": "Workflow Id", "sortable": False, "fieldOrder": 61, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchReason", "displayText": "Workflow Reason", "sortable": False, "fieldOrder": 62, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchState", "displayText": "Workflow State", "sortable": False, "fieldOrder": 63, "selected": False, "sortOrder": 0, "sortType": "ASC" }, { "identifierField": "workflowBatchUserNote", "displayText": "Workflow State User Note", "sortable": False, "fieldOrder": 64, "selected": False, "sortOrder": 0, "sortType": "ASC" } ] } ] }

    # Send API request to the platform
    print(api_url)
    
    try:
        response = requests.post(api_url, headers=header, data=json.dumps(body))
        print("Export request submitted successfully.")
        logging.info("Export request submitted successfully.")
        jsonified_response = json.loads(response.text)
        export_identifier = jsonified_response['id']

    except:
        print("There was an error requesting your export.")
        logging.error("There was an error requesting your export.")
        print(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        logging.error(f"Response Text: {response.text}")
        exit(1)

    return export_identifier


def download_exported_file(platform, key, client, export, filename):

    """
    Downloads an export via the RiskSense REST API.

    :param platform:    URL of the RiskSense platform to be queried.
    :type  platform:    str

    :param key:         API Key
    :type  key:         str

    :param client:      Client ID associated with the export.
    :type  client:      int

    :param export:      Identifier of the export to be downloaded.
    :type  export:      int

    :param filename:    File path and name where download will be stored.
    :type  filename:    str

    :return:    Returns a boolean reflecting whether or not the download was successful.
    :rtype:     bool
    """

    success = False

    #  Assemble the URL for the API call
    url = platform + "/api/v1/client/" + str(client) + "/export/" + str(export)

    #  Define the header for the API call
    header = {
        'x-api-key': key,
        'content-type': 'application/json'
    }

    print("Attempting to download your export file.")
    logging.info("Attempting to download your export file.")
    

    #  Send API request to the platform
    try:
        response = requests.get(url, headers=header)
        print("Writing your file to disk.")
        logging.info("Writing your file to disk.")
        open(filename, "wb").write(response.content)
        print(" - Done.")
        os.remove("assessment_name.txt")
        success = True

    except:
        print("There was an error getting your file.")
        logging.error("There was an error getting your file.")
        print(f"Response Status Code: {response.status_code}")
        logging.error(f"Response Status Code: {response.status_code}")
        print(f"Response Text:{response.text}")
        logging.error(f"Response Text:{response.text}")
        os.remove("assessment_name.txt")
        exit(1)

    return success


def read_config_file(filename):

    """
    Reads TOML-formatted configuration file.

    :param filename:    path to file to be read.
    :type  filename:    str

    :return:    Variables found in config file.
    :rtype:     dict
    """
    try:
        toml_data = open(filename).read()
        data = toml.loads(toml_data)
    except FileNotFoundError:
        print("Wrong file or file path (or)File 'config_export.toml' does not exist")
        logging.info("Wrong file or file path (or) File 'config_export.toml' does not exist")
        exit(1)
        
    return data


def main():

    """ Main body of the script. """
    
    """ Logging """
    
   
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', 'export_findings.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)    
    logging.basicConfig(filename=log_file, level=logging.DEBUG,format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    #  Read config file to get platform info and API token
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config_export.toml')
    configuration = read_config_file(conf_file)
    try:
        assessment_name = open('assessment_name.txt').readlines()
           
    except FileNotFoundError:
        print("Wrong file or file path (or) File 'assessment_name.txt' doesn't exist")  
        logging.info("Wrong file or file path (or) File 'assessment_name.txt' doesn't exist")  
        exit(1)
    assessment_name = ''.join(assessment_name)
    #print(assessment_name)
    # Set our variables based on what is read from the config file.

    rs_url = configuration['platform']['url']
    api_key = configuration['platform']['api_key']
    client_id = configuration['platform']['client_id']
    file_name = configuration['platform']['file_name']
    if rs_url == '':
        rs_url = sys.argv[2]  
    if api_key == '':   
        api_key = sys.argv[4]
    if client_id == '':   
        client_id = sys.argv[6]
    if file_name == '':   
        file_name = sys.argv[8]   


    # getting the timestamp
    
    #input from the user to save it as a file
    #export_filename= configuration['platform']['file_name']
    #assessment = configuration['platform']['file_name']
    
    
    ######################################
    #  Start file export
    ######################################

    #  Initiate the export.  Export ID is returned.
    export_id = initiate_export(rs_url, api_key, client_id, file_name,assessment_name)
    #print(export_id)
    #  Wait for file to be exported.  This could take quite a while depending now how big
    #  your export is, and how busy the platform is.  You may need to adjustaccordingly.
    #  Currently set to wait 5 minutes.
    wait_time = 25  # Seconds
    counter = 0

    # Display a countdown timer while we wait for the platform to generate the export file.
    while counter < wait_time:
        if counter == 0:
            print(f" - Sleeping for {wait_time - counter} seconds to allow the platform some time to generate the file.")
            logging.info(f" - Sleeping for {wait_time - counter} seconds to allow the platform some time to generate the file.")
        time.sleep(1)
        counter += 1

    ######################################
    #  Download exported file
    ######################################

    #  This is the location to save your exported file.  Adjust as desired.
    #  Hostfindings exports are zip files containing other files with the actual findings.

    exported_path_file = file_name + '.zip'
    
    # Request download from the platform.
    downloaded = download_exported_file(rs_url, api_key, client_id, export_id, exported_path_file)

    if downloaded:
        print("Success.")
        logging.info("Success.")
        
        
        # Download the exported zip file 

        with zipfile.ZipFile(exported_path_file, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(exported_path_file)
        
        ts = date.today()
        ts = str(ts).replace(' ','')
        #print(ts)
        folder = file_name + str(ts)
        current_directory = os.getcwd()
        
        final_directory = os.path.join(current_directory, folder)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
            
        os.replace("Assets.csv", final_directory+"/Assets.csv")
        os.replace("Findings.csv", final_directory+"/Findings.csv")
        
        
    else:
        print("There was an error downloading your export file from the platform.")
        logging.info("There was an error downloading your export file from the platform.")
        exit(1)


#  Execute the Script
if __name__ == "__main__":
    main()

"""
   Copyright 2019 RiskSense, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
