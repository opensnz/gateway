#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update

# 1. Install python package manager
sudo apt install -y pip

# 3. Install all dependencies of the project
# WorkingDirectory=/home/pi/PacketForwarder
sudo pip install paho-mqtt
########## Packet Forwarder Service Daemon Installation ############

# 1. Create file packetforwarder.service and paste the following lines
[Unit]
Description=Packet Forwarder Service Daemon
StartLimitIntervalSec=86400
StartLimitBurst=8640

[Service]
User=pi
Group=sudo
Type=simple
WorkingDirectory=/home/pi/PacketForwarder
ExecStart=/usr/bin/python3 -u /home/pi/PacketForwarder/forwarder.py
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target

# 2. Copy packetforwarder.service to /lib/systemd/system/ folder
sudo cp /home/pi/PacketForwarder/packetforwarder.service /lib/systemd/system/packetforwarder.service

# 3. Give rights on packetforwarder.service file to pi user
sudo chmod 644 /lib/systemd/system/packetforwarder.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable packetforwarder service
sudo systemctl enable packetforwarder.service

# 6. Start packetforwarder service
sudo systemctl start packetforwarder.service


####### Other commands ##########

# Restart packetforwarder service
sudo systemctl restart packetforwarder.service

# Show packetforwarder service status
sudo systemctl status packetforwarder.service

#  Show packetforwarder service journal 
sudo journalctl -r -u packetforwarder.service