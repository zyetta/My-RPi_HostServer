# My-RPi Host Server

![GitHub repo size](https://img.shields.io/github/repo-size/zyetta/My-RPi_HostServer?style=for-the-badge)

![GitHub last commit](https://img.shields.io/github/last-commit/zyetta/My-RPi_HostServer)

***
## My-RPi Host Server.
Central application used to manage and monitor the power state of paired Hubs and RPis.

### Inforamtion
All packages and dependacies have been pre-configured, appart from the following which require manual configuration.

#### 1. SSH Certificates


| Item      | Folder / Filename |
| --- | ----------- |
| Folder      | ./rpi_monitor/mirpi/ssh_certificates       |
| Public Key   | id_rsa2.pub        |
| Private Key   | id_rsa2
#### 2. Email Credentials

| Item      | Folder / Filename |
| --- | ----------- |
| Folder      | ./rpi_monitor/mirpi      |
| Constants   | cnst.py         |

#### 3. Deploy Code
```sh
cd ./
sudo docker-compose up --build
```

#### 4. Database Table Creation
For the inital deployment, the **rpi_monitor** scheme has be be created. 
This is done with the following lines of code where the default database credentials are as follow
```sh
username: root
password: "K9x21A8BPERAFBYEAkeASnlHkpgE9lghaEksnR8hVXm01yh"
```

```sh
docker exec -it MySQL bash
mysql -u root -p
root_pass #Enter when Prompted
#Finally, create the database
CREATE DATABASE network_rpi;
#Exit MySQL, and the container, and restart the Web-Application
EXIT;
EXIT;
docker restart My-RPi
```

Once the scheme has been created, My-RPi may be restarted and the tables will automatically be created, and accessible on port 80.

***
# GUI
## Dashboard
![Imgur](https://i.imgur.com/hvlLdC1.png)
![Imgur](https://i.imgur.com/yaFlBqe.png)


## Device Management
![Imgur](https://i.imgur.com/fZkB561.png)
## Hub Management
![Imgur](https://i.imgur.com/N3pE8JU.png)
## Preferences
![Imgur](https://i.imgur.com/QrJOT1C.png)

***
# References
This package comprises the following software infrastructure:
- [MariaDB](https://mariadb.org/)
- [Flask](https://palletsprojects.com/p/flask/)
- [Highcharts](https://www.highcharts.com/)
- [Pandas](https://pandas.pydata.org/)
- [NMap](https://nmap.org/)
- [Numpy](https://numpy.org/)
- [Parimiko](https://github.com/pallets/flask)
- [Nginx](https://www.nginx.com/)
- [MQTT](https://mqtt.org/)

