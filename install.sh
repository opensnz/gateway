echo "Installation of Encoder Service..."
cd ./Encoder
sudo chmod a+x ./encoder.sh
source ./encoder.sh
cd ..
echo "Finished"

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
cd ..
echo "Finished"


<<<<<<< HEAD
echo "Installation of Transceiver Service..."
cd ./Transceiver
sudo chmod a+x ./transceiver.sh
source ./transceiver.sh
cd ..
echo "Finished"


=======
>>>>>>> e56b0b64581c7934506678f3284ff90b378e6b67
echo "Installation of Interface Service..."
cd ./Interface
sudo chmod a+x ./interface.sh
source ./interface.sh
cd ..
echo "Finished"