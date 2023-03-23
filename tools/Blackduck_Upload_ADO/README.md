## Requirements

 - Python 3
    - This script has been tested using Python 3.9.6
 - Install dependecy modules using pip package



## Overview

A python script creates ADO Ticket for each vulnerability and updates the title and description field of the ticket with necessary information.



### Editing the configuration files:

1. Domain of Risksense Platform needs to be entered inside double quotes (Eg:"platform" or "platform2" or "platform4")

2. ClientID in RiskSense Platform needs to be entered (Eg:815 or 100 etc)

3. RiskSense API Token needs to be entered inside double quotes. It can be generated in "User Settings" page of RiskSense Platform.

4. The following needs to be entered in the Config.xlsx - Group ID, Web app name(App Findings), Project Instance,	Token	User,	Area and Iteration.




##### Running TicketCreation Script:

For Application Findings:
-------------------------
python ADO_ticket_creation_App.py


