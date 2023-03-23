# Rsnotifications_create
A Python script for creating/deleting/disabling delivery channel

----

## Configuration
The configuration file is located at `conf/conf.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

Note :
 1. To delete a channel ensure you provide deletechannel as true in lower case and the disable channel as false in lower case , provide the channelstodeleteid variable with the list of channel ids to delete
 2. To disable a channel ensure you provide disable channel as false in lower case and the disable channel as false in lower case  provide the channelidtodisable variable with the channel id to disable
 3. To create , check and subscribe, keep both the disable channel and delete channel as false and provide the rest of the parameters 

## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 rsnotifications_create.py

 -- OR (depending on your installation) --

python rsnotifications_create.py

The script will perform either one of the following depending on the configuration

1. Delete channel
2. Disabe channel 
3. If no delete or disable , will check create and prompt user for notification to subscribe 

For more understanding of workflow , please view rs notifications workflow.pdf for more info

```