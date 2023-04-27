#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update
# 1. Install 

sudo pip install paho-mqtt

# 2. Configure 


############# Offline Service Daemon Installation ############

# 1. Create file offline.service and paste the following lines

# 2. Copy offline.service to /lib/systemd/system/ folder
sudo cp ./offline.service /lib/systemd/system/offline.service

# 3. Give rights on offline.service file to pi user
sudo chmod 644 /lib/systemd/system/offline.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable offline service
sudo systemctl enable offline.service

# 6. Start offline service
sudo systemctl start offline.service


####### Other commands ##########

# Restart offline service
sudo systemctl restart offline.service

# Show offline service status
sudo systemctl status offline.service

#  Show offline service journal 
sudo journalctl -r -u offline.service