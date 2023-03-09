#################### Project dependencies installation #####################
# 0. Update the source list
sudo apt update
# 1. Install 

pip install requests

# 2. Configure 


############# Gateway Service Daemon Installation ############

# 1. Create file gateway.service and paste the following lines

# 2. Copy gateway.service to /lib/systemd/system/ folder
sudo cp ./gateway.service /lib/systemd/system/gateway.service

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