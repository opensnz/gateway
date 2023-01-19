#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update
# 1. Install 

# 2. Configure 

# 3. Create SQLite folder
sudo mkdir /home/pi/SQLite

############# Gateway Service Daemon Installation ############

# 1. Create file gateway.service and paste the following lines
[Unit]
Description=Gateway Service Daemon
StartLimitIntervalSec=86400
StartLimitBurst=8640

[Service]
User=pi
Group=sudo
Type=simple
WorkingDirectory=/home/pi/Gateway
ExecStart=/usr/bin/python3 -u /home/pi/Gateway/gateway.py
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target

# 2. Copy gateway.service to /lib/systemd/system/ folder
sudo cp /home/pi/Gateway/gateway.service /lib/systemd/system/gateway.service

# 3. Give rights on gateway.service file to pi user
sudo chmod 644 /lib/systemd/system/gateway.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable gateway service
sudo systemctl enable gateway.service

# 6. Start gateway service
sudo systemctl start gateway.service


####### Other commands ##########

# Restart gateway service
sudo systemctl restart gateway.service

# Show gateway service status
sudo systemctl status gateway.service

#  Show gateway service journal 
sudo journalctl -r -u gateway.service