# tag_import_tool

This tool allows a user to mass-create new tags.  The script will read the desired values
from a .csv file, and attempt to create a new tag for each row.


## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.


#### CSV file
An example .csv file has been provided in this folder.  __Do not edit the headers of this file.__

Add a line to this file for each tag you would like created, filling in __all__ fields.

The "owner" value should be the desired user's ID from the platform.  If you would like multiple owners
to be assigned to a new tag, you can provide multiple user IDs.  They should be comma delimited, and
enclosed in double-quotes.  Example: `"1234,5678,4321,8765"`


## Execution
Once you have completed configuration of the script, and completed your .csv file, the script can be run from your
terminal as follows:

```commandline

python3 import_new_tags.py

 -- OR (depending on your installation) --

python import_new_tags.py

```
