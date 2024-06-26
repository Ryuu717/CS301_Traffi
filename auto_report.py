#Send message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Set email address and password
# https://docs.ultralytics.com/guides/security-alarm-system/
password = "ewsl jvzo awpa qjyj"
from_email = "-"  # must match the email used to generate the password
to_email = "-"  # receiver email

server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(from_email, password)

current_time = datetime.datetime.now()
date = current_time.strftime("%m/%d/%Y %H:%M:%S")


# Speeding Report
def send_email(object_detected, speed):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "Security Alert"
    
    # Add in the message body
    message_body = f'ALERT - {object_detected} objects has been detected!!'
    message_body = f'ALERT - Speeding has been detected!! \
                \n Time: {date} \
                \n Location: -- \
                \n Car type: {type} \
                \n Car speed: {speed} km'
                

    message.attach(MIMEText(message_body, 'plain'))
    server.sendmail(from_email, to_email, message.as_string())
    
    
# End User Report
def send_email2(risk_level, location, car_type, plate_number ):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "Security Alert(from End User)"
    
    # Add in the message body
    message_body = f'ALERT - {risk_level} risk level car has been reported!!  \
                \n Time: {date} \
                \n Location: {location} \
                \n Car type: {car_type} \
                \n Plate Number: {plate_number}'
                
    message.attach(MIMEText(message_body, 'plain'))
    server.sendmail(from_email, to_email, message.as_string())