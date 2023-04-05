#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update
# Install dependencies for gateway.py
sudo pip3 install paho-mqtt
sudo pip3 install pyserial
# UART configuration on Pi 3 or 4
############# Edit /boot/config.txt file 
#sudo nano /boot/config.txt
############# Paste these lines at the end of config file
    #### enable_uart=1
    sudo echo "enable_uart=1" >> /boot/config.txt
    ############# For Pi 3
    #### dtoverlay=pi3-disable-bt
    sudo echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt
    ############# For Pi 4
    #### dtoverlay=disable-bt
    #sudo echo "dtoverlay=disable-bt" >> /boot/config.txt
############# Reboot now (after transceiver service enabled)
# sudo reboot


############# Transceiver Service Daemon Installation ############

# 1. Create file transceiver.service and paste the following lines


# 2. Copy transceiver.service to /lib/systemd/system/ folder
sudo cp ./transceiver.service /lib/systemd/system/transceiver.service

# 3. Give rights on transceiver.service file to pi user
sudo chmod 644 /lib/systemd/system/transceiver.service

# 4. Reload linux system daemon manager
sudo systemctl daemon-reload

# 5. Enable transceiver service
sudo systemctl enable transceiver.service

# Reboot now
sudo reboot

#  6. Start transceiver service
# sudo systemctl start transceiver.service


######## Other commands ##########

# Restart transceiver service
# sudo systemctl restart transceiver.service

# Show transceiver service status
# sudo systemctl status transceiver.service

# Show transceiver service journal 
# sudo journalctl -r -u transceiver.service