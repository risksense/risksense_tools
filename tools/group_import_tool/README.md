# group_import_tool

This tool allows a user to mass-create new groups by reading the new group
names from a text file.The script will read the desired values and attempt 
to create a new group for each row in the file.

----

## Configuration

The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

#### Text file
An example text file has been provided in this folder.

Add a line to this file for each Group name you would like to create.


## Execution
Once you have completed configuration of the script, and completed your text file, the script can be run from your
terminal as follows:

```commandline

python3 import_new_groups.py

 -- OR (depending on your installation) --

python import_new_groups.py

```
