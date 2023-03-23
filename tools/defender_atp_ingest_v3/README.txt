""" ***************************************************************************************
|
|  Name        :  README.txt
|  Description :  Documentation for Defender ATP vuln ingestion
|  Copyright   :  2020 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
*************************************************************************************** """

+---------------+
|    Purpose    |
+---------------+----------------------------------------------------------------------------
This script is to assist in the retrieval and RiskSense platform ingestion of Defender
ATP data.


+----------------+
|    Overview    |
+----------------+---------------------------------------------------------------------------
This script will attempt to retrieve Defender ATP host and vulnerability data.  It will
then correlate the vuln data with the associated host data.  This data is then written
to a CSV file to be ingested by the RiskSense Generic Uploader.  Upon completion of the
data correlation, the script will attempt to upload the data to the RiskSense platform,
creating a new assessment and upload in the process.

A mapping for this CSV file should be created prior to the first run of this script,
else the ingestion will not complete, calling for the mapping to be completed first.


+--------------------+
|    Requirements    |
+--------------------+-----------------------------------------------------------------------
A working installation of Python3 (and pip) is required.  Additionally, the following
Python packages are required:

    * TOML
    * Requests
    * ProgressBar2
    * argparse

These packages can be installed by navigating your terminal to the base folder of this
script and running the following command:

    $ pip install -r requirements.txt

        --- OR (depending on your Python/pip installation) ---

    $ pip3 install -r requirements.txt


+----------------------------------+
|    Installation/Configuration    |
+----------------------------------+----------------------------------------------------------
To install this script, simply unzip the zip file in the desired location, and install
the required packages using the instructions above.

The configuration of this script can be found in conf/config.toml.  Open this file with
your text editor of choice for editing.  You will see the following:

    [risksense_platform]
        url = 'https://platform.risksense.com'
        api_key = ''

    [defender]
        token_url = ''
        client_id = ''
        client_secret = ''

    [output]
        file_folder = 'output_files'

    [upload_to_platform]
        # Specify the path to the folder containing the files you wish to upload.
        # If you update this, please use the absolute path to your desired folder.
        files_folder = 'files_to_process'

        # Trigger URBA upon completion of upload processing.
        auto_urba = true

        # You may uncomment this parameter and enter the desired network ID for
        # your upload here if you already know it.
        network_id = 123456  # UPDATE ME

        # You may uncomment this parameter and enter the desired client ID for your
        # upload here if you already know it.
        client_id = 654321  # UPDATE ME

    [debug]
        write_raw_json_responses = false

NOTE that api_key, token_url, tenant_id, client_id and client_secret will be set through
the arguments passed to the script, in that order.

The rest of the values however will still be fetched from the conf/config.toml file. 




+-------------+
|    Usage    |
+-------------+----------------------------------------------------------------------------
To execute the script, navigate your terminal to the base script folder, and run the
following command:


    $ python main.py --rsapikey Your_RiskSense_API_Key --tokenurl https://api.securitycenter.microsoft.com  --tenatid Your_Defender_TenantID --clientid Your_Defender_ClientID --secret Your_Defender_ClientSecret
        --- OR (depending on your Python installation) ---

    $python3 main.py --rsapikey Your_RiskSense_API_Key --tokenurl Your_Defender_TokenURL --tenatid Your_Defender_TenantID --clientid Your_Defender_ClientID --secret Your_Defender_ClientSecret


