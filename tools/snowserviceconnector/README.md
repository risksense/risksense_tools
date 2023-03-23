# snow_service_connector_create
A Python script for creating a Service Now Service type connector in Risksense platform.

----

## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

 * `platform_url` - Risksense platform URL (eg: https://platform2.risksense.com)
 * `api_key` - Risksense API Key (eg: xxxxxxxxxx)
 * `client_id` - Risksense Client ID (eg: 123)
 * `snow_url` - JIRA platform URL (eg: https://xyz.atlassian.net)
 * `snow_username` - JIRA username (eg: xyz@orgs.com)
 * `snow_password_or_api_token` - JIRA API token or password (eg: xxxxxx)
 * `snow_connector_name` - JIRA connector name to be created in Risksense platform


## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 main.py
 -- OR (depending on your installation) --

python main.py

```

__NOTE : The User has to login to the Risksense platform to update other fields in Service Now Incident type connector__
