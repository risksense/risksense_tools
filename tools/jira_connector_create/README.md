# jira_connector_create
A Python script for creating a JIRA connector in Risksense platform.

----

## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

 * `platform_url` - Risksense platform URL (eg: https://platform2.risksense.com)
 * `api_key` - Risksense API Key (eg: xxxxxxxxxx)
 * `client_id` - Risksense Client ID (eg: 123)
 * `jira_url` - JIRA platform URL (eg: https://xyz.atlassian.net)
 * `jira_username` - JIRA username (eg: xyz@orgs.com)
 * `jira_password_or_api_token` - JIRA API token or password (eg: xxxxxx)
 * `jira_connector_name` - JIRA connector name to be created in Risksense platform


## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 jira_connector_create.py

 -- OR (depending on your installation) --

python jira_connector_create.py

```


## Limitation
This script updates the following in connector's fields while creating the connector
 * Updates Connetor Name.
 * Updates Username.
 * Updates Location (URL)
 * Updates Token / Password.
 * Updates Project.
 * Updates Issue Type.
 * Updates Priority as `NoPrio`.
 * Use `plugin information` for Summary.
 * Use `plugin information` for Description.
 * Updates Tag Type.
 * Set `Ticket Close State`.
 * Set `Ticket Sync State`.
 * Check in `Move the Jira Issue to the selected "Closed Status" above when all associated findings for a ticket are in a closed state in Risksense` option.

__NOTE : The User has to login to the Risksense platform to update other fields in JIRA connector__