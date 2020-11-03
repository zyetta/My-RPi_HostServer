# My-RPi Host Server

![GitHub repo size](https://img.shields.io/github/repo-size/zyetta/My-RPi_HostServer?style=for-the-badge)

![GitHub last commit](https://img.shields.io/github/last-commit/zyetta/My-RPi_HostServer)

***
## My-RPi Host Server.
The central application used to manage and monitor the power state of paired Hubs and RPis.

### Inforamtion
All packages and dependencies have been pre-configured, apart from the following which requires manual configuration.

### Pre-requisites
All packages and dependencies have been pre-configured, apart from the following which requires manual configuration. Listed below are software dependacies for the Host Machine.

- [Docker (Option 1) - Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Docker (Option 2) - Windows](https://docs.docker.com/docker-for-windows/install/)
- [Docker (Option 3) - Mac](https://docs.docker.com/docker-for-mac/install/)
- [Docker (Option 4) - Raspberry Pi](https://phoenixnap.com/kb/docker-on-raspberry-pi)
- [Docker Compose](https://www.tutorialspoint.com/docker/docker_compose.htm)

### Installation Guide

#### 1. SSH Certificates

[Generate](https://www.youtube.com/watch?v=vpk_1gldOAE) your own SSH certificats **Without a password**, and paste them in the 'ssh_certificates' folder. 
![Imgur](https://i.imgur.com/zNpACbt.png)





#### 2. Email Credentials
Insert your own network configuration into the 'cnst.py' file. network configurations should not need alteration, if using the entire docker-compose build, but email credentials will need alteration.
![Imgur](https://i.imgur.com/AGJizHQ.png)

##### 3. Deploy Code
Transfer files to RPi, or host machine of choice. If running on laptop / pc with docker. This can be skipped.


##### 4. Deploy Code
SSH into host machine, cd to program directory, and deploy code.

```sh
cd ./
sudo docker-compose up --build
```
![Imgur](https://i.imgur.com/wx0q7G3.png)


##### 5. Database Table Creation (For first deployment)
For the initial deployment, the **rpi_monitor** scheme must be created after the code has been built.


This can be done with the following lines of code, or through MySQL workbench
```sh
#Variables to use
root_user: root
root_pass: "K9x21A8BPERAFBYEAkeASnlHkpgE9lghaEksnR8hVXm01yh"
```

```sh
docker exec -it MySQL bash
mysql -u root_user -p
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

