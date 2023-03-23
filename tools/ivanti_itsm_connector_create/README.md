# ivanti_itsm_connector_create

## Requirements

 - Python 3
    - This script has been tested using Python 3.10.2
 - Run this command to install all dependency modules -> `pip install -r requirements.txt`.
 - The `config.toml` file should be configured before running the script.


## Overview

 - A Python script for creating a Ivanti ITSM connector in Risksense platform.


## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

 * `platform_url` - Risksense platform URL (eg: https://platform2.risksense.com)
 * `api_key` - Risksense API Key (eg: xxxxxxxxxx)
 * `client_id` - Risksense Client ID (eg: 123)
 * `itsm_url` - Ivanti ITSM platform URL (eg: https://xyz.abc.com)
 * `itsm_api_token` - Ivanti ITSM API token or password (eg: xxxxxx)
 * `itsm_connector_name` - Ivanti ITSM connector name to be created in Risksense platform


## Execution
Once you have completed configuration of the script, the script can be run from your
terminal as follows:

```commandline

python3 ivanti_itsm_connector_create.py

 -- OR (depending on your installation) --

python ivanti_itsm_connector_create.py

```
