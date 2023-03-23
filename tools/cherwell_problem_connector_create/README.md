# cherwell_problem
A Python script for creating a cherwell problem connector in Risksense platform.

----

## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

 * `platform_url` - Risksense platform URL (eg: https://platform2.risksense.com)
 * `api_key` - Risksense API Key (eg: xxxxxxxxxx)
 * `client_id` - Risksense Client ID (eg: 123)
 * `cherwell_url` - Cherwell platform URL (eg: https://xyz.atlassian.net)
 * `cherwell_username` - Cherwell username (eg: xyz@orgs.com)
 * `cherwell_password` - Cherwell password (eg: xxxxxx)
 * `cherwell_name` - Cherwell connector name to be created in Risksense 
 * `cherwell_clientidkey` - Cherwell client id key to be created in  

## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 main.py

 -- OR (depending on your installation) --

python main.py

```
The terminal will pop out field values for each dynamic drop down fields,for ticket description fields,supported description fields where you can choose the necessary values that you want to add while creating the connector . 

## Limitation
This script updates the following in connector's fields while creating the connector
__NOTE : The User has to login to the Risksense platform to update other fields in Cherwell problem type connector__
__NOTE : When priority field arrives in dynamicfield detail, please specify between 1 to 5__
