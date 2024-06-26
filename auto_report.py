#Send message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


password = "ewsl jvzo awpa qjyj"
from_email = "ishiryuuu17@gmail.com"  # must match the email used to generate the password
to_email = "ishiryuuu17@gmail.com"  # receiver email

server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(from_email, password)

current_time = datetime.datetime.now()
date = current_time.strftime("%m/%d/%Y %H:%M:%S")



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
                

    
    # message_detail = ""
    # for i in object.trk_idslist:
    #     car_track_id = i
    #     car_type = object.detected_cars[i]
    #     car_speed = object.detected_cars[i]
    #     car_exceeding_speed = object.detected_cars[i]
    #     car_direction = object.detected_cars[i]
        
    #     message_detail + f"Date: {date} \n"
    #     message_detail + f"Car Track ID: {car_track_id} \n"
        
    
    # message_body = f'ALERT - Speeding has been detected!! \ 
    #                 \n{message_detail}'
            

    message.attach(MIMEText(message_body, 'plain'))
    server.sendmail(from_email, to_email, message.as_string())
    
    
    
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