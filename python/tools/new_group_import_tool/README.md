# group_import_tool

This tool allows a user to mass-create new groups.  The script will read the desired values
from a text file, and attempt to create a new group for each row.


## Requirements
A working Python 3 installation is required.  This script has been tested using Python 3.7.2.

The `risksense_api` module is required.


## Configuration
#### Text file
An example text file has been provided in this folder.

Add a line to this file for each Group name you would like to create.


#### Script
Using your favorite text editor, open `conf/config.toml` file.  
* Update the `platform_url` variable value to reflect the RiskSense platform you use.
* Update the `api_key` variable value to reflect your API key.  You can generate an API key from the User Settings page
  in the RiskSense platform UI.
* Update the `group_text_filename` variable value to reflect the path to your text file that contains the group names.
* If you are a single-client user, there is no need to uncomment and update the `client_id` variable value.  If you are a multi-client
  user, you will need to edit the `client_id` variable value to reflect the ID of the client you wish to work with.


```python
platform_url = 'https://platform.risksense.com'

api_key = ''

group_text_filename = 'text_file_example.csv'

# If you are a single-client user, leave this setting alone.
# If you are a multiclient user, uncomment setting, and specify the
# the client ID that you wish to work with.

#client_id = 12345
```

## Execution
Once you have updated the configuration, and completed your text file, the script can be run from your
terminal as follows:

```commandline

python3 import_new_groups.py

 -- OR (depending on your installation) --

python import_new_groups.py

```
