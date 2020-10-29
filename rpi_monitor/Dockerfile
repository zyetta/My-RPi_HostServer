FROM zyetta/debian_python:latest
WORKDIR /mirpi
ADD . /mirpi

RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install nmap -y
CMD ["uwsgi", "app.ini"]
