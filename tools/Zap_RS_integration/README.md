## Requirements

 - Python 3
    - This script has been tested using Python 3.7
 - Python Modules (recommend to install using pip):
    - toml
    - urllib3
    - requests
    - progressbar2
    - zipfile
    - datetime
	- json
	- time
	- os
	
	
_Note : The scripts upload_to_platform and export_findings can be run in both ways ; command line and config based approach ( by placing required values in config files )_

# upload to platform


***Config based approach**

Usage : Pre - requisites :

Provide the necessary parameters in the conf/config_upload.toml file , which are :
	* Platform
	* Api Key
	* Network ID
	* Client ID
	* files to process
	
Run : python upload_to_platform.py

(or)

***Command line** 

can be run by command line arguments entirely by,

# Example

python upload_to_platform.py -p <platform-url> -a <api-key> -f files_to_process -n <network-id> -c <client-id> 
 

Outcome : The scan results will be uploaded to the intended platform and the client. Once this is run , the data can be exported from Riksense by,

# Export_RS_application_findings
This is to export the Risksense Application findings using RS API's


	
**Config based approach**

**Steps to export the results**

* Provide the necessary parameters in config_export.toml file under conf/config_export.toml.
  * Platform
  * API key
  * Client ID
  * Assessment name
  * File name to export
  
Now, Run : python export_findings.py  


(or)
 
**Command line**

 We can run this by means on command line parameters entirely by ,
 
 
# Example
 
python export_findings.py -p <platform-url> -a <api-key> -c <client-id> -f <file-name> (make sure the order of the command line arguments is same)

Note : The assessment name in this program would be from the previously run script that will upload the results into the platform , so no need to provide it as a separate argument.

Outcome:

* You will see that the scan results with Assets and Findings will be placed in a folder with the current date
