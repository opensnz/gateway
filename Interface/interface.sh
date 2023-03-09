
sudo pip install Flask 
sudo pip install psutil


############# Interface Service Daemon Installation ############

# 1. Create file interface.service and paste the following lines

# 2. Copy interface.service to /lib/systemd/system/ folder
sudo cp ./interface.service /lib/systemd/system/interface.service

# 3. Give rights on interface.service file to pi user
sudo chmod 644 /lib/systemd/system/interface.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable interface service
sudo systemctl enable interface.service

# 6. Start interface service
sudo systemctl start interface.service


####### Other commands ##########

# Restart interface service
sudo systemctl restart interface.service

# Show interface service status
sudo systemctl status interface.service

#  Show interface service journal 
sudo journalctl -r -u interface.service