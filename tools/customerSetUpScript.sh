#! /bin/sh

# Set script to output commands being ran
set -x

wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

mv ./cloudflared-linux-amd64 /usr/local/bin/cloudflared

chmod a+x /usr/local/bin/cloudflared

cloudflared update

# Move the required files to the directory we created.
mv *.yml *.json /usr/local/bin

# Install the cloudflared service to run cloudflared as a service.
cloudflared --config /usr/local/bin/config.yml service install

systemctl start cloudflared

# Enable tunnel to start on boot.
systemctl enable cloudflared

systemctl status cloudflared

# Start and enable the auto update timer for cloudflare
systemctl start cloudflared-update.timer

systemctl enable cloudflared-update.timer

systemctl status cloudflared-update.timer
