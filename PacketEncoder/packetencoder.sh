#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update

# 1. Install npm
sudo apt install -y npm

# 2. Install the latest nodejs on Raspberry Pi through n
sudo npm install -g n
sudo n latest
########## restart bash terminal
########## check npm and node versions
sudo node -v
sudo npm -v
########## Remove npm of step 1
sudo apt remove npm
sudo apt autoremove

# 3. Install all dependencies of the project
# Go to Project Directory : /home/pi/PacketEncoder
sudo npm install

########## Packet Encoder Service Daemon Installation ############

# 1. Create file packetencoder.service and paste the following lines
[Unit]
Description=Packet Encoder Service Daemon
StartLimitIntervalSec=86400
StartLimitBurst=8640

[Service]
User=pi
Group=sudo
Type=simple
WorkingDirectory=/home/pi/PacketEncoder
ExecStart=npm start
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target

# 2. Copy packetencoder.service to /lib/systemd/system/ folder
sudo cp /home/pi/PacketEncoder/packetencoder.service /lib/systemd/system/packetencoder.service

# 3. Give rights on packetencoder.service file to pi user
sudo chmod 644 /lib/systemd/system/packetencoder.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable packetencoder service
sudo systemctl enable packetencoder.service

# 6. Start packetencoder service
sudo systemctl start packetencoder.service


####### Other commands ##########

# Restart packetencoder service
sudo systemctl restart packetencoder.service

# Show packetencoder service status
sudo systemctl status packetencoder.service

#  Show packetencoder service journal 
sudo journalctl -r -u packetencoder.service