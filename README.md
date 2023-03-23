# risksense_tools

A repository of tools that interact with the RiskSense API.

## Available Tools

* **appfinding_report_from_saved_filter**
  * A tool for generating a csv report based upon a saved filter in the platform.
* **tag_import_tool**
  * A tool for the mass creation of new tags via the reading of a .csv file.
* **cmdb_update_tool**
  * A tool for the mass update of hosts' CMDB information via the reading of a .csv file.
* **group_import_tool**
  * A tool for the mass creation of new groups via the reading of a .csv file.
* **hostfinding_report_from_saved_filter**
  * A tool for generating a csv report based upon a saved filter in the platform.
* **asset_criticality_update**
  * A tool for updating assets' criticalities via reading of a csv file.
* **create_and_assigntags**
  * A tool used to create remediation and assign host findings tags
* **burpsuite_create**
  * A tool used to create burpsuite connector
* **delete_hosts_in_defaultgroup**
  * A tool that is used to delete the hosts data from default group
* **deletes_app_sindefaultgroup**
  * A tool that is used to delete apps in default group
* **Groupbyexport**
  * A tool that is used to export data in groupby
* **hclappscan_connector_create**
  * A tool used to create hcl appscan connector
* **jira_connector_create**
  * A tool for creating a JIRA connector in Risksense platform.
* **nessusconnector create**
  * A tool for creating nessus connectors in product/demo risksense platforms
* **nexposeconnector create**
  * A tool for creating nexpose connectors in product/demo risksense platforms
* **qualyspcconnector_create**
  * A tool for creating qualys policy compliance connectors in product/demo risksense platforms
* **qualysvmconnector_create**
  * A tool for creating qualys vmdr connector connectors in product/demo risksense platforms
* **qualysvulnconnector_create**
  * A tool for creating qualys vulnerability connectors in product/demo risksense platforms
* **qualyswasconnector_create**
  * A tool for creating qualys web application connectors in product/demo risksense platforms
* **rs3simulator**
  * A tool for simulating rs3 score for assets in risksense
* **slacreation**
  * A tool for creating sla in platform
* **exportslahf**
  * A tool for exporting hostfindings that based on sla in platform
* **slapriority**
  * A tool for getting priority of a particular sla in platform
* **snow_incident_connector_create**
  * A tool for creating a Service Now Incident type connector in Risksense platform.
* **sonarcloudconnector_create**
  * A tool for creating sonar cloud connectors in product/demo risksense platforms
* **awsinspectorcreate**
  * A tool for creating aws inpsector connectors in product/demo risksense platforms
* **cherwell_incident_connector_create**
  * A tool for creating cherwell incident connectors in product/demo risksense platforms
* **cherwell_makerequest_connector_create**
  * A tool for creating cherwell make request connectors in product/demo risksense platforms
* **cherwell_problem_connector_create**
  * A tool for creating cherwell problem connectors in product/demo risksense platforms    
* **grouptools**
  * A tool that list groups,create,assign,edit,delete and assign users
* **ivanti_itsm_connector_create**
  * A tool that creates ivanti itsm connector using user input
* **ivanti_itsm_ticket_creation**
  * A tool that create ivanti itsm ticket using user input
* **jira_ticket_creation**
  * A tool that create ivanti itsm ticket using user input
* **snow_incident_ticket_creation**
  * A tool that create ivanti itsm ticket using user input
* **snow_service_request_ticket_creation**
  * A tool that create ivanti itsm ticket using user input
* **applicationsecuritydashboard**
  * This tool will display data from the application security dashboard
* **executivedashboard**
  * This tool will display data from the executive dashboard
* **prioritization_dashboard**
  * This tool will display data from theprioritization dashboard based on the input provided by you in the terminal
* **ransomewaredashboard**
  * This tool will display data from the ransomware dashboard based on the input provided by you in the terminal
* **sla overview dashboard**
  * This tool will display data from the sla overview dashboard based on the input provided by you in the terminal
* **checkmarxosaconnector**
  * Tool for creating checkmarx osa connector
* **checkmarxsastconnector**
  * Tool for creating checkmarx sast connector
* **expander_connector**
  * Tool for creating Palo Alto Xpanse Expander connector
* **falconspotlightconnector***
  * Tool for creating Crowdstrike falcon spotlight connector
* **ivanti_itsm_connector_create**
  * Tool for creating Ivanti ITSM connector
* **nexposeassettag**
  * Tool for creating Nexpose asset tag connector
* **qualysasset**
  * Tool for creating Qualys asset connector
* **snowctcconnector_create**
  * Tool for creating Snow CTC connector
* **whitehatconnector_create**
  * Tool for creating Whitehat connector  
* **snowserviceconnector**
  * Tool for creating Snow SR connector
* **veracodeconnector_create**
  * Tool for creating veracode connector
* **Aquasec**
  * Tool for creating aquasec connector
* **Sonatype**
  * Tool for creating Sonatype connector
* **Fortifyondemand**
  * Tool for creating Fortifyondemand connector



## Test Cases

## Requirements
* A working [Python 3](https://python.org) installation is required.
* Additionally, the following Python packages are required:
  * [TOML](https://pypi.org/project/toml/)
  * [Requests](https://pypi.org/project/requests/)
  * [Progressbar2](https://pypi.org/project/progressbar2/)
  * [rich](https://pypi.org/project/rich/)
  
The required packages can be installed with the following command:

    pip install -r requirements.txt

***Or***, depending on your installation of Python/Pip:

    pip3 install -r requirements.txt


## Installation
Download zip file, copy the file to the desired location, and unzip.

## Library Package Documentation
https://demo-risksense-tools.readthedocs.io/en/latest/
