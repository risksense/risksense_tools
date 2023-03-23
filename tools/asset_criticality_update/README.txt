""" ***************************************************************************************
|
|  Name        :  README.txt
|  Description :  Documentation for 'asset_criticality_update'
|  Copyright   :  2021 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
*************************************************************************************** """

+---------------+
|    Purpose    |
+---------------+----------------------------------------------------------------------------
This script is to assist in the mass-updating of the asset criticality of hosts in
the RiskSense platform.


+----------------+
|    Overview    |
+----------------+---------------------------------------------------------------------------
This script will read a CSV file to determine the appropriate asset criticality settings
for hosts in the RiskSense platfrom, and update them accordingly via the API.

The CSV file should have only two columns: 'hostname' and 'criticality'. An example CSV
file named 'criticalities_example.csv' has been included in the folder containing this script.


+----------------------------------+
|    Configuration    |
+----------------------------------+----------------------------------------------------------
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.


+-------------+
|    Usage    |
+-------------+----------------------------------------------------------------------------
To execute the script, navigate your terminal to the base script folder, and run the
following command:

    $ python main.py

        --- OR (depending on your Python installation) ---

    $python3 main.py