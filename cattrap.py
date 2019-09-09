from picamera import PiCamera
from time import sleep
from gpiozero import Servo
from gpiozero import Button
from gpiozero import LED
from gpiozero import OutputDevice as stepper
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ftplib
import urllib.request

#data from database
cellnum = ''
em = ''
trapid = '8165010001'
# end data from database

#
trapdata = {}

detector = Button(23)

flashone = LED(26)
flashtwo = LED(19)

p1 = stepper(12)  # orange
p2 = stepper(16)  # purple
p3 = stepper(20)  # red
p4 = stepper(21)  # brown  

cam = PiCamera()



def ftpupload():
    server = 'ftp.zachariahferguson.com'
    username = 'trapper@zachariahferguson.com'
    password = '*******************'
    ftp_connection = ftplib.FTP(server, username, password)
    fh = open(trapid + '.jpg', 'rb')
    ftp_connection.storbinary('STOR ' + trapid + '.jpg', fh)
    fh.close()
    ftp_connection.close()

def sendtext(cellnum):
    print('texting...')

    account_sid = 'ABC123DEF456HIJ789KLM012NOP345QRS6'
    auth_token = '802f2875cea9098fe940fa9ae506f6b9'
    auth_token = '********************************'
    client = Client(account_sid, auth_token)

    #message info!!!!!!!!!!!!!!!!!!!!!!!!!

    message = client.messages \
            .create(
                body="Look who's in your trap! Go to www.zachariahferguson.com/cattrap-cgi.html to access trap controls.",
                from_='+15707261627',
                media_url='https://zachariahferguson.com/trapper/' + trapid + '.jpg',
                to='+1' + cellnum
            )
    print(message.sid)
    print('texted to: ' + cellnum)
    print('image location: https://zachariahferguson.com/trapper/' + trapid + '.jpg')

def sendemail(em):
    print('emailing: ' + em)
    msg = MIMEMultipart()
    msg['From'] = 'catcatcher@zachariahferguson.com'
    msg['To'] = em
    password = '**********************'
    msg['Subject'] = "Look who you've caught!"
    body = 'Hello from the catcatcher. This is who is in your trap right now:<br><img src="https://www.zachariahferguson.com/trappe/r"' + trapid + '.jpg"><br><a href="www.zachariahferguson.com/cattrap-cgi.com">Click here to access the trap controls.</a>'
    filename = trapid + '.jpg'
    attachment = open('/home/pi/Documents/cattrap/' + trapid + '.jpg', "rb")
    msg.attach(MIMEText(body, 'html'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    #ports ssl: 465, non-ssl: 2525
    server = smtplib.SMTP('zachariahferguson.com', 2525)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def feed():
    def coil_traverse(timeinc):
        p1.on()
        p2.off()
        p3.off()
        p4.off()
        sleep(timeinc)
        p1.off()
        p2.on()
        p3.off()
        p4.off()
        sleep(timeinc)
        p1.off()
        p2.off()
        p3.on()
        p4.off()
        sleep(timeinc)
        p1.off()
        p2.off()
        p3.off()
        p4.on()
        sleep(timeinc)

    def rotate(cycles, timer):
        p1.off()
        p2.off()
        p3.off()
        p4.off()
        x = 0
        while x < cycles:
            coil_traverse(timer)
            x += 1
        p1.off()
        p2.off()
        p3.off()
        p4.off()

    rotate(90, 0.005)
    return

def activate():
    # drop gate and lock
    print('gate lock servo')
    servo_lock.min()
    sleep(0.5)
    servo_lock.max()
    sleep(0.5)
    servo_lock.mid()
    sleep(5)

def reset():
    # unlock gage, raise gate
    print('gate raise servo')
    servo_gate.min()
    sleep(0.5)
    servo_gate.max()
    sleep(0.5)
    servo_gate.mid()
    sleep(5)

def piccapture():
    cam.start_preview()
    sleep(3)
    cam.capture('/home/pi/Documents/cattrap/' + trapid + '.jpg')
    cam.stop_preview()

def snapshot():

    flashone.on()
    flashtwo.on()
    piccapture()
    sleep(1)
    flashone.off()
    flashtwo.off()
    ftpupload()
    #sleep(2)  # give file time to upload before texting link

def data_gather():
    global trapdata
    trapdata = {}
    received = []
    html = urllib.request.urlopen('https://zachariahferguson.com/cgi-bin/pi-ctcgi.py?serial=' + trapid).read()
    trapkeys = ['serial', 'cellnum', 'email', 'status', 'activate', 'reset', 'feed', 'foodcount', 'image']
    html = str(html)
    lines = html.split('class="pdata"')
    vars = lines[1:10]
    for item in vars:
        b = item.find(' ') + 1
        neweritem = item[b:]
        e = neweritem.find('<')
        newestitem = neweritem[:e]
        received.append(newestitem)
    count = 0
    while count < len(trapkeys):
        trapdata[trapkeys[count]] = received[count]
        count += 1


def update_record(field, value):
    html = urllib.request.urlopen('https://zachariahferguson.com/cgi-bin/pi-dbcgi.py?serial=' + trapid + '&' + field + '=' + value).read()
    return

def handler():
    # after data is gathered from the server, this function checks if gathered data is different from what was stored.
    # if different data exists, it takes action (updates variables or performs functions)
    # if a function was performed, it changes the initiating True back to a False in the database

    global cellnum, trapid, em, trapdata

    # check for updates to cell number, implement
    if cellnum != trapdata['cellnum']:
        cellnum = trapdata['cellnum']
        print('cell number updated.')
        return
		
    # check for updates to email, impliment
    if em != trapdata['email']:
        em = trapdata['email']
        print('email updated.')
        return
	
    # check if instruction to feed has been sent, if yes, run feeder, then reset to false
    if trapdata['feed'] == 'True':
        feed()
        update_record('feed', 'False')
        print('feeder activated')
        return

    # check if new image requested, if yes, upload, and reset to false
    if trapdata['image'] == 'True':
        snapshot()
        update_record('image', 'False')
        print('image updated')
        return
    
    # check if instruction to reset (release animal) has been sent, if yes, run feeder, then reset to false
    if trapdata['reset'] == 'True':
        reset()
        update_record('reset', 'False')
        print('release command received.')
        return

    # check if instruction to reset ( animal) has been sent, if yes, run feeder, then reset to false
    if trapdata['activate'] == 'True':
        activate()
        update_record('activate', 'False')
        return

def main():
    print('starting detection loop.')
    x = 0
    sleep_timer = 2
    sleep(3)
    print('initialized')
    flashone.off()
    flashtwo.off()
    while True:
        try:
            sleep(sleep_timer)
            # no animal present; check for changes or new commands
            data_gather()
            #print('connected to network. updates received...')
            # act on changes or commands
            handler()

            # test for presense of an animal
            if detector.is_pressed:
                d = 1
                print('beam broken')
                for y in range(1, 9):
                    sleep(0.2)
                    if detector.is_pressed:
                        d += 1
                    if detector.is_pressed is False:
                        d -= 1
                    if d > 5:
                        print('capturing image of trap occupant...')
                        snapshot()
                        
                        if em != "":
                            sendemail(em)
                        if cellnum != "":
                            sendtext(cellnum)
        except:
                print('no network link. Waiting 60 seconds...')
                sleep(60)



main()
