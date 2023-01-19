#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update
# 1. Install paho-mqtt and pyLoRa module and its dependencies
sudo pip install RPi.GPIO
sudo pip install spidev
sudo pip install pyLoRa

# 2. Enable SPI peripheral
sudo raspi-config

# 3. Create 

############# Transceiver Service Daemon Installation ############

# 1. Create file transceiver.service and paste the following lines
[Unit]
Description=Transceiver Service Daemon
StartLimitIntervalSec=86400
StartLimitBurst=8640

[Service]
User=pi
Group=sudo
Type=simple
WorkingDirectory=/home/pi/Transceiver
ExecStart=/usr/bin/python3 -u /home/pi/Transceiver/transceiver.py
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target

# 2. Copy transceiver.service to /lib/systemd/system/ folder
sudo cp /home/pi/Transceiver/transceiver.service /lib/systemd/system/transceiver.service

# 3. Give rights on transceiver.service file to pi user
sudo chmod 644 /lib/systemd/system/transceiver.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable transceiver service
sudo systemctl enable transceiver.service

# 6. Start transceiver service
sudo systemctl start transceiver.service


####### Other commands ##########

# Restart transceiver service
sudo systemctl restart transceiver.service

# Show transceiver service status
sudo systemctl status transceiver.service

#  Show transceiver service journal 
sudo journalctl -r -u transceiver.service