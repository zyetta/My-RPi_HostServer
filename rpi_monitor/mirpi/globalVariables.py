device_ping =           60
curr_state_period =     10      
EMAIL_ADDRESS =         'zyetta01@gmail.com'                             #Email Server Email
EMAIL_PASSWORD =        'CxBwY0Dt7d9kDiep9UtpD5rsF2YlMyLurdJHuTJsPze9LPhkaP'                                            #Email Server Password
network_scanning_timer = 60                                                  #Network Scanning Timer
broker_address=         "mosquitto"                                             #MQTT Broker
broker_port =           1883                                                    #MQTT Port
refresh_rate =          1                                                       #MQTT Refresh Rate
time_out =              45                                                      #MQTT Timeout
username =              'mqtt'                                                  #MQTT Broker Username
password =              'gJGResE%0puwsX8%V$tp*01z2RJz0u88OFdjkDyO7*V0Yjo'       #MQTT Broker Password

CERT = './mirpi/ssh_certificates/id_rsa2.pub'                                    #Public Certificate Directory
CERTPVT = './mirpi/ssh_certificates/id_rsa2'                                     #Private Certificate Directory
LEDFILE = './mirpi/rpi/shutdown_script.py'                                                   #LED FILE Directory
PINGFILE = './mirpi/rpi/resource_check.py'                                       #Resource Checking FIle Directory
UPLOAD_FOLDER = './mirpi/uploads/'                                               #CSV Upload Type Directory
ALLOWED_EXTENSIONS = set(['csv'])                                               #Only Listen for CSV

