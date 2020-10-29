apt-get update
apt-get install python3-pip -y
sudo pip3 uninstall gpiozero -y
sudo pip3 uninstall paho-mqtt -y
sudo pip3 uninstall psutil -y
sudo pip3 install gpiozero 
sudo pip3 install paho-mqtt 
sudo pip3 install psutil

python3 ./control/resource_check.py