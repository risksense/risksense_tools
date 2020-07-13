# tag_import_tool

This tool allows a user to mass-create new tags.  The script will read the desired values
from a .csv file, and attempt to create a new tag for each row.

## Requirements
A working Python 3 installation is required.  This script has been tested using Python 3.7.2.

The `risksense_api_python` module is required.

## Configuration
#### CSV file
An example .csv file has been provided in this folder.  __Do not edit the headers of this file.__

Add a line to this file for each tag you would like created, filling in __all__ fields.

The "owner" value should be the desired user's ID from the platform.  If you would like multiple owners
to be assigned to a new tag, you can provide multiple user IDs.  They should be comma delimited, and
enclosed in double-quotes.  Example: `"1,2,3,4,5"`

#### Script
Near the top of the `import_tags.py` file, locate the configuration area as shown below.  
* Update the `PLATFORM_URL` variable value to reflect the RiskSense platform you use.
* Update the `API_KEY` variable value to reflect your API key.  You can generate an API key from the User Settings page
  in the RiskSense platform UI.
* If you are a single-client user, there is no need to update the `CLIENT_ID` variable value.  If you are a multi-client
  user, you will need to edit the `CLIENT_ID` variable value to reflect the ID of the client you wish to work with.
* Update the `TAG_CSV_FILENAME` variable value to reflect the path to your .csv file.

```python
# ==== BEGIN CONFIGURATION ============================================================================================

#  URL for your platform.
PLATFORM_URL = 'https://platform.risksense.com'

#  Your API key.  Can be generated on your user settings page when logged in to the RiskSense platform.
API_KEY = ''

#  If you are a single-client user, there is no need to edit the CLIENT_ID variable.
#  If you are a multi-client user, specify the client ID you wish to work with here.
#  Example:
#  CLIENT_ID = 12345
CLIENT_ID = None

#  Path to CSV file to read tag info from.
TAG_CSV_FILENAME = 'csv_file_example.csv'

#  No need to edit the line below.
PROFILE = risksense_api_python.Profile('user_profile', PLATFORM_URL, API_KEY)

# ==== END CONFIGURATION ==============================================================================================
```

## Execution
Once you have completed configuration of the script, and completed your .csv file, the script can be run from your
terminal as follows:

```commandline

python3 import_tags.py

 -- OR (depending on your installation) --

python import_tags.py

```
