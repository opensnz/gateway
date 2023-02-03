#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update

# 1. Install python package manager
sudo apt install -y pip

# 3. Install all dependencies of the project
# WorkingDirectory=/home/pi/gateway/Forwarder
sudo pip install paho-mqtt
########## Packet Forwarder Service Daemon Installation ############

# 1. Create file forwarder.service and paste the following lines

# 2. Copy forwarder.service to /lib/systemd/system/ folder
sudo cp /home/pi/gateway/Forwarder/forwarder.service /lib/systemd/system/forwarder.service

# 3. Give rights on forwarder.service file to pi user
sudo chmod 644 /lib/systemd/system/forwarder.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable forwarder service
sudo systemctl enable forwarder.service

# 6. Start forwarder service
sudo systemctl start forwarder.service


####### Other commands ##########

# Restart forwarder service
sudo systemctl restart forwarder.service

# Show forwarder service status
sudo systemctl status forwarder.service

#  Show forwarder service journal 
sudo journalctl -r -u forwarder.service