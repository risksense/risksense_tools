# snow_connector_create
A Python script for creating a Service Now Custom table configuration type connector in Risksense platform.

----

## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

 * `platform_url` - Risksense platform URL (eg: https://platform2.risksense.com)
 * `api_key` - Risksense API Key (eg: xxxxxxxxxx)
 * `client_id` - Risksense Client ID (eg: 123)
 * `snow_url` - SNOW platform URL (eg: https://xyz.atlassian.net)
 * `snow_username` - SNOW username (eg: xyz@orgs.com)
 * `snow_password_or_api_token` - SNOW API token or password (eg: xxxxxx)
 * `snow_connector_name` - SNOW connector name to be created in Risksense
 * `tablename` - SNOW platform URL (eg: https://xyz.atlassian.net)
 * `statusfield` - SNOW username (eg: xyz@orgs.com)
 * `ticketidfield` - SNOW API token or password (eg: xxxxxx)


## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 snowctcconnector_create.py

 -- OR (depending on your installation) --

python snowctcconnector_create.py

```

## Working

You must enter table field data and other data when it prompts in the terminal 
