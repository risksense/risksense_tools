#Overview

This script polls the project data from Synopsys Polaris and ingests them all into Risksense Platform.

# conf/config_polaris.toml

[polaris]
token = "" # Enter the API Token of polaris
file = "file_test" Can be left as it is(not necessary to change , since its just a temporary file to get exported into)

Example:

[polaris]
token = "sampleapikey"
file = "file_test"


# upload_to_platform-master_branch\conf\config.toml

Enter the Risksense Platform URL , API key and client ID in config.toml file under "upload_to_platform-master_branch\conf" ; 

* platform = 'https://platform4.risksense.com' 
* api-key = 'xxxx'   ---> to be generated in Risksense platform for a user.
* client_id = 1373 ( Ivanti DevSecOps client )
* network_id = 12345 --> Finding Network ID ; You can find the network id by using POST API (https://xxxx.risksense.com/api/v1/client/{client_id}/network) Json Body : {"name": "polaris","type": "IP"} , Header ; Key - x-api-key , Value - xxxx

Once these values are entered, you can run the script as;

python main.py "option"

"option" can be ;
O - Opened , C - Closed , A - All 


Example :

* python main.py C
* python main.py O

 
======================================================================================================================================

Developed by;

Prasanth Bharadhwaaj ,
Yugesh ,
Jai Balaji ,
Security Analyst - CSW.