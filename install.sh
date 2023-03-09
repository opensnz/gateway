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


echo "Installation of Interface Service..."
cd ./Interface
sudo chmod a+x ./interface.sh
source ./interface.sh
cd ..
echo "Finished"