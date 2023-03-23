# ROSA V2 Customer Set Up Script

This script is used to quickly deploy a Cloudflare ROSA tunnel using the JSON and Config.yml files we provide.

# Requirements
Before attempting to run this script you will need to have received a JSON and Config.yml files from Ivanti. These files are needed to authenticate and configure your specific tunnel to connect to our Cloudflare edge. In addition the location you attempt to deploy Cloudflare's agent needs to have access to the services you are attempting to set up connectors for. If you would like to minimize the access that the Cloudflare agent has you can use the following information on the ports and IP's needed for the agents access: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/configuration/ports-and-ips/

# Running the CustomerSetUpScript.sh

This script is performing the following steps:
1. Downloading the last cloudflare agent from: https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
2. Moving this .deb file to /usr/local/bin/cloudflared and updating its execution permissions.
3. Moving the .yml and .json files we supplied with it to /usr/local/bin
4. Installing Cloudflared (Cloudflare's agent) as a service
5. Starting the service, enabling it to start on boot, and displaying its status.
6. Starting the auto-update service, enabling it to start on boot, and displaying its status.

To run the script you will want to elevate your access to Root and then run "bash CustomerSetUpScript.sh".

# Useful Commands
You can use the following commands to interact with the Cloudflared service if needed

Get the service status: sudo systemctl status cloudflared

Stopping the service: sudo systemctl stop cloudflared

Restarting the service: sudo systemctl restart cloudflared