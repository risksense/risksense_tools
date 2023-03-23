## appfinding_report_from_saved_filter

A python script that will gather all application findings using a saved 
application finding filter, and write the results to a .csv file.

----
## Configuration

The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.


## Execution
Once you have completed configuration of the script, the script can be 
run from your terminal as follows:

```commandline

python3 app_finding_report_from_filter.py

 -- OR (depending on your installation) --

python app_finding_report_from_filter.py

```