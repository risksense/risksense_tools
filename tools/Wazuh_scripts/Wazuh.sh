# ==========================================================================================================================================
# This script is used to pull the data from Splunk and push it to the Risksense Platform
# Usage --> sh ./Wazuh.sh <option>
# 'option' can be , "C" - Critical , "H" - High , "M" - Medium or "L" - Low
# ==========================================================================================================================================

#!/bin/bash
if [ "$1" == "C" ]
then
  python3 splunk_data.py  C
elif [ "$1" == "H" ]
then
  python3 splunk_data.py  H
elif [ "$1" == "M" ]
then
  python3 splunk_data.py  M
elif [ "$1" == "L" ]
then
  python3 splunk_data.py  L
fi

mv Data*.csv upload_to_platform/files_to_process

python3 upload_to_platform/upload_to_platform.py 
