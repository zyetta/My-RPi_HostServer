#Time Periods
pingPeriod =            60      #Device Ping Period [s]
safeShutdown =          10      #Safe shutdown delay
netScanTime =           60      #Network Scanning Timer [s]
totPowerSamp =          600     #Resample period for total power calculation

#MQTT Broker Credentials
broker_address =         ["10.42.0.2", "localhost", "mosquitto", "192.168.137.2"]       #MQTT Broker(s)
broker_port =           1883                                                            #MQTT Port
broker_refreshRate =          1                                                         #MQTT Refresh Rate
broker_timeOut =              45                                                        #MQTT Timeout
broker_username =              'mqtt'                                                   #MQTT Broker Username
broker_password =              'gJGResE%0puwsX8%V$tp*01z2RJz0u88OFdjkDyO7*V0Yjo'        #MQTT Broker Password

#MySQL Credentials
mysql_user = 'root'
mysql_password = 'K9x21A8BPERAFBYEAkeASnlHkpgE9lghaEksnR8hVXm01yh'
mysql_table = 'network_rpi'
mysql_server = 'localhost'

#Email Server Credentials
EMAIL_ADDRESS =         'name@gmail.com'                                                #Email Server Email
EMAIL_PASSWORD =        ''                                                              #Email Server Password


#File Directories
CERT = './mirpi/ssh_certificates/id_rsa2.pub'                                           #Public Certificate Directory
CERTPVT = './mirpi/ssh_certificates/id_rsa2'                                            #Private Certificate Directory
LEDFILE = './mirpi/rpi/shutdown_script.py'                                              #LED FILE Directory
PINGFILE = './mirpi/rpi/resource_check.py'                                              #Resource Checking FIle Directory
TEMP = './mirpi/uploads/'                                                               #CSV Upload Type Directory
ALLOWED_EXTENSIONS = set(['csv'])                                                       #Only Listen for CSV
