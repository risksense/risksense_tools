## Requirements

 - Python 3
    - This script has been tested using Python 3.10.2
 - Run this command to install all dependency modules -> `pip install -r requirements.txt`.
 - The `config.toml` file should be configured before running the script.


## Overview

 - This python script creates a ServiceNow Incident Ticket for findings selected using commands in CLI.


## Editing the configuration file conf/config.toml

 - Configurable parameters for `RS_Platform_Configuration` section are:
	- `platform` : Add the platform URL. It accepts only __string__ values and case sensitive.
	- `apiToken` : Add the API Token. It can be generated in the RiskSense UI, under User Settings. It accepts only __string__ values and case sensitive.
	- `clientID` : Enter the client ID. It accepts only __integer__ values.	 
	- `SNOWConnectorName` : Enter the ServiceNow Incident connector Name. It accepts only __string__ values and case sensitive.


```toml
---  EXAMPLE  ---

[RS_Platform_Configuration]
	platform = "https://platform.risksense.com" # Risksense Platform needs to be filled
	clientID = 111        # Client ID in RiskSense Platform needs to be filled
	apiToken = "xxxxxxxxxxxx"         # API token of RiskSense Platform accont needs to be filled	
	SNOWConnectorName = "SNOW Test Task Type"     # Configured ServiceNow Incident connector in RS Platform

```

## Script workflow

 - The user is prompted with a question for which `finding type` the ticket should be created for.
 - Then the user has to set `Active Filters` using user inputs to filter out findings the ticket should be created for.
 - The script will display the finding count associated with the set Active Filters. If the count is zero then the script will exit with the necessary error message.
 - Now the user has to fill the Ticket Form fields using user inputs. If invalid user input is entered then the script will exit with the necessary error message.
 - Now the user is prompted with a question for selecting `Tag type`.
 - Then the ServiceNow Incident ticket is created and its `ticket ID` is displayed in the terminal.


##### Running main.py:
```python
 $ python3 main.py

      (or)
      
 $ python main.py
```