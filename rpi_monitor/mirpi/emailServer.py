from email.message import EmailMessage
import smtplib
import mirpi.cnst as const

# Title:     Test Mail
# Desc:      Test Mail sent to predetermined email address
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def testMail(RECIEVER):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] Test Message'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')

    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>Pew Pew!</h1>
            Test email Successful!
        </body>
    </html>
    """, subtype='html')
    print("Sent")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)


# Title:     Shutdown Device (ALL)
# Desc:      Notification when all devices are shutdown in preferences
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def ShutdownAll(RECIEVER):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] Shutdown All Devices'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')

    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>Kill Switch Enabled</h1>
            All Devices will be shutdown
        </body>
    </html>
    """, subtype='html')
    print("Sent")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)

# Title:     New Device Added
# Desc:      Notification Sent to Email when a new device has been added to teh database
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def NewDeviceAdded(RECIEVER, ip, mac, hub, hub_location, username, date_added, hostname):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] New Device Added'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')
    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>New Device Added</h1>
            Textfile of new devices information is attached below.<br>
            <hr>
            This message has been automatically generated from My-RPi, a Network, and Power monitor for RPi's developed by JJ MAREE (Github: Zyetta).
        </body>
    </html>
    """, subtype='html')

    def NewDeviceAdded_NP(**kwargs):
        template = """Date Added:   {date_added}
Hostname:   {hostname}
IP Address: {ip} 
MAC Address:    {mac}
Username:   {username}
HUB:    {hub}
HUB Pin:    {hub_location}
        """
        filename = "./emails/" + "NewDeviceAdded" + ".txt"
        with open(filename, 'w') as yfile:
            yfile.write(template.format(**kwargs))
    keywords = {'ip': ip, 'mac': mac, 'hub': hub, 'hub_location': hub_location,
                'username': username, 'date_added': date_added, 'hostname': hostname}
    NewDeviceAdded_NP(**keywords)
    with open('./emails/NewDeviceAdded.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename="DeviceData.txt")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)

# Title:     CPU Temperature Limit Exceeded
# Desc:      CPU Temperature from device scans has exceeded pre-defined limit
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def CPUTempExceeded(RECIEVER, ip, mac, hub, hub_location, username, date_added, hostname, cpu_temp, mem_used, pcu_used, mem_tot):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] CPU Temperature Exceeded'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')
    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>CPU Temperature Exceeded</h1>
            Textfile of new devices information is attached below.<br>
            <hr>
            This message has been automatically generated from My-RPi, a Network, and Power monitor for RPi's developed by JJ MAREE (Github: Zyetta).
        </body>
    </html>
    """, subtype='html')

    def CPUTempExceeded_NP(**kwargs):
        template = """Date Added:   {date_added}
Hostname:   {hostname}
IP Address: {ip} 
MAC Address:    {mac}
Username:   {username}
HUB:    {hub}
HUB Pin:    {hub_location}
CPU Temperature:    {cpu_temp}
CPU Usage:  {pcu_used}
MEM Usage:  {mem_used}
MEM Total:  {mem_tot}
        """
        filename = "./emails/" + "CPUTempExceeded" + ".txt"
        with open(filename, 'w') as yfile:
            yfile.write(template.format(**kwargs))

    keywords = {'ip': ip, 'mac': mac, 'hub': hub, 'hub_location': hub_location, 'username': username,
                'date_added': date_added, 'hostname': hostname, 'cpu_temp': cpu_temp, 'pcu_used': pcu_used,
                'mem_used': mem_used, 'mem_tot': mem_tot}

    CPUTempExceeded_NP(**keywords)
    with open('./emails/CPUTempExceeded.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename="DeviceData.txt")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)

# Title:     Current Limit Exceeded
# Desc:      Notification Sent when the current stored Via MQTT is greater than a predefined threshold
# Author:    JJ MAREE
# Last Mod:  01-07-2020


def CurrLimitExceeded(RECIEVER, ip, mac, hub, hub_location, username, date_added, hostname, curr, volt):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] Current Exceeded'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')
    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>Max Current Exceeded</h1>
            Textfile of new devices information is attached below.<br>
            <hr>
            This message has been automatically generated from My-RPi, a Network, and Power monitor for RPi's developed by JJ MAREE (Github: Zyetta).
        </body>
    </html>
    """, subtype='html')

    def CPUTempExceeded_NP(**kwargs):
        template = """Date Added:   {date_added}
Hostname:   {hostname}
IP Address: {ip} 
MAC Address:    {mac}
Username:   {username}
HUB:    {hub}
HUB Pin:    {hub_location}
Current Measured:   {curr}
Voltage Measured:   {volt}
        """
        filename = "./emails/" + "CurrentExceed" + ".txt"
        with open(filename, 'w') as yfile:
            yfile.write(template.format(**kwargs))

    keywords = {'ip': ip, 'mac': mac, 'hub': hub, 'hub_location': hub_location, 'username': username,
                'date_added': date_added, 'hostname': hostname, 'curr': curr, 'volt': volt}

    CPUTempExceeded_NP(**keywords)
    with open('./emails/CurrentExceed.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename="DeviceData.txt")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)


# Title:     New Device Found In Network Scans
# Desc:      Notification sent when New Device Found In Network Scans
# Author:    JJ MAREE
# Last Mod:  01-07-2020
def NewFound(RECIEVER, IP, MAC, TYPE, DATE_ADDED):
    msg = EmailMessage()
    msg['Subject'] = '[Mi-RPi] Network Scan Updates'
    msg['From'] = const.EMAIL_ADDRESS
    msg['To'] = RECIEVER
    msg.set_content('message_body')
    msg.add_alternative("""\
    <!DOCKTYPE html>
    <html>
        <body>
            <h1>Network Scan Updates</h1>
            Textfile of new devices information is attached below.<br>
            <hr>
            This message has been automatically generated from My-RPi, a Network, and Power monitor for RPi's developed by JJ MAREE (Github: Zyetta).
        </body>
    </html>
    """, subtype='html')

    def NEW(**kwargs):
        template = """Date Added:   {date_added}
        IP Address: {ip} 
        MAC Address:    {mac}
        Type (1 = New / 0 = Update):   {up_type}
        """
        filename = "./emails/" + "NewScan" + ".txt"
        with open(filename, 'w') as yfile:
            yfile.write(template.format(**kwargs))

    keywords = {'ip': IP, 'mac': MAC, 'up_type': TYPE,
                'date_added': DATE_ADDED}

    NEW(**keywords)
    with open('./emails/NewScan.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application',
                       subtype='octet-stream', filename="DeviceData.txt")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(const.EMAIL_ADDRESS, const.EMAIL_PASSWORD)
        smtp.send_message(msg)
