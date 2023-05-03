echo "Installation of Mosquitto Service..."
cd ./Mosquitto
sudo chmod a+x ./mosquitto.sh
source ./mosquitto.sh
cd ..
echo "Finished"

echo "Installation of Forwarder Service..."
cd ./Forwarder
sudo chmod a+x ./forwarder.sh
source ./forwarder.sh
cd ..
echo "Finished"

echo "Installation of Gateway Service..."
cd ./Gateway
sudo chmod a+x ./database.sh
source ./database.sh
sudo chmod a+x ./gateway.sh
source ./gateway.sh
sudo chmod a+x ./offline.sh
source ./offline.sh
cd ..
echo "Finished"

echo "Installation of Interface Service..."
cd ./Interface
sudo chmod a+x ./interface.sh
source ./interface.sh
cd ..
echo "Finished"

echo "Installation of Transceiver Service..."
cd ./Transceiver
sudo chmod a+x ./transceiver.sh
source ./transceiver.sh
cd ..
echo "Finished"