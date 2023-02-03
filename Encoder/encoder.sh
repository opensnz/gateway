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
# Go to Project Directory : /home/pi/Encoder
sudo npm install

########## Packet Encoder Service Daemon Installation ############

# 1. Create file encoder.service and paste the following lines
[Unit]
Description=Packet Encoder Service Daemon
StartLimitIntervalSec=86400
StartLimitBurst=8640

[Service]
User=pi
Group=sudo
Type=simple
WorkingDirectory=/home/pi/Encoder
ExecStart=npm start
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target

# 2. Copy encoder.service to /lib/systemd/system/ folder
sudo cp /home/pi/Encoder/encoder.service /lib/systemd/system/encoder.service

# 3. Give rights on encoder.service file to pi user
sudo chmod 644 /lib/systemd/system/encoder.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable encoder service
sudo systemctl enable encoder.service

# 6. Start encoder service
sudo systemctl start encoder.service


####### Other commands ##########

# Restart encoder service
sudo systemctl restart encoder.service

# Show encoder service status
sudo systemctl status encoder.service

#  Show encoder service journal 
sudo journalctl -r -u encoder.service