#################### mosquitto installation #####################
# 0. Update the source list
sudo apt update
# 1. Install mosquitto
sudo apt install mosquitto -y

# 2. Configure mosquitto :
##### open mosquitto.conf 
#sudo nano /etc/mosquitto/mosquitto.conf
##### specify password file (paste these lines in mosquitto.conf)
#password_file /etc/mosquitto/passwd
#listener 1883
sudo chmod a+w /etc/mosquitto/mosquitto.conf
sudo echo "password_file /etc/mosquitto/passwd" >> /etc/mosquitto/mosquitto.conf
sudo echo "listener 1883" >> /etc/mosquitto/mosquitto.conf

# 3. Create password file
#sudo touch /etc/mosquitto/passwd
sudo cp ./passwd /etc/mosquitto/passwd

# 4. Generate password for clients (username, password must be modified)
#sudo mosquitto_passwd -b /etc/mosquitto/passwd username password

# 5. Restart mosquitto service
sudo systemctl restart mosquitto.service

# 6. Show mosquitto service status
sudo systemctl status mosquitto.service