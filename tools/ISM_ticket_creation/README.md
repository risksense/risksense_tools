# Requirements

*  Use ‘pip3 install -r requirements.txt’ to install all dependencies present in the requirements.txt file.

# conf/config.toml

* There are some parameters to be put in inside config.toml file which are in the format ;

[platform]
    "url" = '' # Add the url of the platform
    "api_key" = ''  # Add your API key here.
    "client_id" =   # Update to include your client ID here.(no single quotes to be provided here).
    "file_name" = '' # Not necessary to change/add anything here.
    "tag_prefix"= '' # Prefix in the tag created in the riksense that the script looks for .
    "incident_prefix" = '' # Prefix in the tag that will be renamed in the riksense post ticket creation.
    "tag_owner" = '' # Valid Owner(userid) who will be changing the tag name post ticket creation.
	
	
[ISM]
	"ism_url" = 'https://ism-csmriptide-tenant1.ivanticlouddev.com/api/odata/businessobject/incidents'   # incident creation url
	"ism_attachment_url" = 'https://ism-csmriptide-tenant1.ivanticlouddev.com/api/rest/Attachment'   # attachment url
	"ism_key" = ''   # ism API Key
	"assignee_prefix" = ''   # Prefix in the tag created in the riksense that the script looks for to assign to a person.
	"default_assignee"= '' # Assignee to whom the ticket would be assigned , if the script doesn't find any assignee's name in the created tag.
	"profile_link"= '' # Profile link of a user in ISM(depends on user who is creating tickets)


Once the paramaters are entered in config.toml file , run the script as ;

# Incident Creation

Description :

This script is used to get the tags from the Risksense platform to export the findings present in it, once extracted , a ticket is created with the required data in Ivanti ISM, once a ticket is created, the tag name is replaced with the Incident ID from the ITSM.

Running the script:

*python Ticket_system.py*
