from flask import Flask, render_template, Response,jsonify,request,session, flash, redirect, url_for

#FlaskForm--> it is required to receive input from the user
# Whether uploading a video file  to our object detection model

from flask_wtf import FlaskForm
from forms import UserReportForm, UserRegistrationForm, UserLoginForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
# from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from wtforms import FileField, SubmitField,StringField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os

from datetime import date, timedelta
import pandas as pd


# Required to run the YOLOv8 model
import cv2

from db_handler import db_select, db_select_where, db_select_where_above, db_select_count_data_by_day, db_select_count_speedings_by_day, db_select_count_camera_by_status, db_insert_user_report, db_insert_users, check_password, db_select_where_above_by_month, db_update_cars
from ultralytics.solutions.speed_estimation import SpeedEstimator


# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from YOLO_Video import video_detection
# from predict import predict
from predict2 import predict2


app = Flask(__name__)

app.secret_key = 'random string'

app.config['SECRET_KEY'] = 'ryuu'
app.config['UPLOAD_FOLDER'] = 'static/files'


################################################################################################
# Session
################################################################################################
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


################################################################################################
# Class
################################################################################################
class User(UserMixin):
   def __init__(self, UserID, FirstName, LastName, Phone, Email, Password, Role, Authorized, Status, UserType):
      self.UserID = UserID
      self.FirstName = FirstName
      self.LastName = LastName
      self.Phone = Phone
      self.Email = Email
      self.Password = Password
      self.Role = Role
      self.Authorized = Authorized
      self.Status = Status
      self.UserType = UserType
      self.authenticated = False
      
   def is_anonymous(self):
      return False
   def is_authenticated(self):
      return self.authenticated
   def is_active(self):
      return True
   def get_id(self):
      return self.UserID
   def get_user_type(self):
      return self.UserType

# class Admin(User):
#    UserType = "Admin"

# class Operator(User):
#    UserType = "Operator"



#Use FlaskForm to get input video file  from user
class UploadFileForm(FlaskForm):
    #We store the uploaded video file path in the FileField in the variable file
    #We have added validators to make sure the user inputs the video in the valid format  and user does upload the
    #video when prompted to do so
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)
        

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')



def generate_frames2(path_x = ''):
   yolo_output = predict2(path_x)
   # print(f"yolo_output::::::::::::::::::{yolo_output}")
   for detection_ in yolo_output:
      # print(f"detection_::::::::::::{detection_}")
      ref,buffer=cv2.imencode('.jpg',detection_)

      frame = buffer.tobytes()
      # print(f"frame::::::::::{frame}")
      yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')



# def generate_frames_web2(path_x):
#     yolo_output = predict(path_x)
#     for detection_ in yolo_output:
#         ref,buffer=cv2.imencode('.jpg',detection_)

#         frame=buffer.tobytes()
#         yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

################################################################################################
# Login manager
################################################################################################
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(UserID):
   user_info = db_select_where("*", "Users", "UserID", UserID)
   # if user_info is None:
   if user_info == []:
      return None
   else:
      return User(int(user_info[0][0]), user_info[0][1], user_info[0][2], user_info[0][3], user_info[0][4], user_info[0][5], user_info[0][6], user_info[0][7], user_info[0][8], user_info[0][9])




################################################################################################
# Test
################################################################################################
# @app.route('/test')
# def test():
#         return render_template('chart.html', data={"Name":"Salary", "Mike":10000, "Jim":800, "Alice":12500,"Bob":7000})


# HTML
# {% for k, v in data.items() %}



################################################################################################
# Traffic API
################################################################################################
# Tomtom
# https://developer.tomtom.com/traffic-api/documentation/traffic-incidents/incident-details#https-method-get




################################################################################################
# Landing Page
################################################################################################
@app.route("/")
def landing():
   return render_template("landing.html")


################################################################################################
# Sign up
################################################################################################
@app.route("/signup")
def signup():
   
   form = UserRegistrationForm()
    
   if request.method == 'POST': 
      if form.validate() == False: 
         flash('All fields are required.') 
         return render_template('signup.html', form = form) 
      else: 
         return render_template('index.html') 
   
   if request.method == 'GET': 
      return render_template('signup.html', form = form) 

################################################################################################
# Log in
################################################################################################
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if request.method == 'POST': 
        if form.validate() == False: 
            flash('All fields are required.') 
            return render_template('login.html', form = form) 
        else: 
            # 0. Current user
            current_user_id = str(current_user.get_id())
            user_info = db_select_where("*","Users", "UserID", current_user_id) 
            return render_template('index.html',
                                   user_info = user_info) 
    
    if request.method == 'GET': 
        return render_template('login.html', form = form) 

################################################################################################
# Log out
################################################################################################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing'))



################################################################################################
# Dashbords
################################################################################################
@app.route("/dashboard", methods=['GET', 'POST'])
def main():
   # session.clear()
   
   # 0. Current user
   current_user_id = str(current_user.get_id())
   print(f"current_user_id::::::::::{current_user_id}")
   user_info = db_select_where("*","Users", "UserID", current_user_id)  
   
   
   selected_month = 1
   if request.method == 'POST':
      selected_month = request.form['mySelect']
   
    
   # 1. All Records
   all_records = db_select("*","AllRecords")

   # 2. Number of cars by month
   car_list = db_select_where("*","AllRecords", "Month", selected_month)  
   num_cars = (len(car_list))
   
   # exceeding_rate = db_select_where("exceedingRate","AllRecords", "exceedingRate", 0)
   # exceeding_rate = db_select_where_above("*","AllRecords", "ExceedingRate", 20)
   exceeding_rate = db_select_where_above_by_month("*","AllRecords", "ExceedingRate", 20, selected_month)
   num_exceedings = len(exceeding_rate)
   
   
   #the number of data by days on January
   dayly_count_list = db_select_count_data_by_day("Day","AllRecords", selected_month)  
   
   data1 = [['Date', 'Count']]
   for i in range(len(dayly_count_list)):
      list = []
      list.append(dayly_count_list[i][0])
      list.append(dayly_count_list[i][1])
      data1.append(list)
      
      
   #the number of data by speedings and days on January
   daily_speeding_list = db_select_count_speedings_by_day("Location","AllRecords", selected_month)  
   
   data2 = [['Location', 'Count']]
   for i in range(len(daily_speeding_list)):
      list = []
      list.append(daily_speeding_list[i][0])
      list.append(daily_speeding_list[i][1])
      data2.append(list)

   #the number of accident on January
   data3 = [
      ['Type', 'Numbers'],
      ['Speedings',     11],
      ['Crush',      2],
      ['Slip',  2],
      ['Drunk', 2],
      ['Drug',    7]
   ]
   
   #the number of data by speedings and days on January
   camera_status_list = db_select_count_camera_by_status("Status","Cameras", "Status")  
   
   data4 = [['Status', 'Counts']]
   for i in range(len(camera_status_list)):
      list = []
      list.append(camera_status_list[i][0])
      list.append(camera_status_list[i][1])
      data4.append(list)
   
   
   #Car Direction Table
   car_direction_list = db_select("*","CarDirection")  
   
   data5 = []
   for i in range(len(car_direction_list)):
      list = []
      list.append(car_direction_list[i][1])
      list.append(car_direction_list[i][2])
      list.append(car_direction_list[i][3])
      list.append(car_direction_list[i][4])
      data5.append(list)

   print(user_info)
   
   return render_template("index.html", 
                          all_records = all_records,
                          num_cars = num_cars,
                          num_exceedings = num_exceedings,
                          data1 = data1,
                          data2 = data2,
                          data3 = data3,
                          data4 = data4,
                          data5 = data5,
                          selected_month = selected_month,
                          user_info = user_info,
                          current_user_id = current_user_id
                          )


################################################################################################
# Live video
################################################################################################
@app.route("/livevideo")
def livevideo():
    #return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
   return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')
   

################################################################################################
# All Records
################################################################################################
@app.route("/allrecords")
def allrecords():
   
   #All records
   all_records = db_select("*","AllRecords")  
   all_records_cols = len(all_records[0])
   
   all_records_temp = []
   for i in range(len(all_records)):
      list = []
      for j in range(all_records_cols):
         list.append(all_records[i][j])
         
      all_records_temp.append(list)
   
      
   return render_template("all_records.html", 
                          all_records = all_records_temp
                          )

################################################################################################
# Cars
################################################################################################
@app.route("/cars")
def cars():
   # Update Cars
   db_update_cars()
   
   #Cars
   car_records = db_select("*","Cars")
   car_records_cols = len(car_records[0])
   
   car_records_temp = []
   for i in range(len(car_records)):
      list = []
      for j in range(car_records_cols):
         list.append(car_records[i][j])
      car_records_temp.append(list)
      
      
   return render_template("cars.html", 
                          car_records = car_records_temp
                          )


################################################################################################
# Map
################################################################################################
@app.route("/map")
def map():
   
   return render_template("map.html", 
                          )
   

################################################################################################
# Analysis
################################################################################################
@app.route('/analysis', methods=['GET','POST'])
def analysis():
   
   # Upload File Form: Create an instance for the Upload File Form
   form = UploadFileForm()
   
   if form.validate_on_submit():
      # Our uploaded video file path is saved here
      file = form.file.data
      file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                              secure_filename(file.filename)))  # Then save the file
      # Use session storage to save video file path
      session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                          secure_filename(file.filename))
      

   return render_template('analysis.html', form=form)



################################################################################################
# Video
################################################################################################
@app.route('/video')
def video():
   # return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
   return Response(generate_frames2(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')
 

################################################################################################
# Traffic Report
################################################################################################
@app.route("/trafficreport")
def trafficreport():
   
   #Traffic Report
   traffic_report = db_select("*","UserReports")  
   traffic_report_cols = len(traffic_report[0])
   num_traffic_report = len(traffic_report)
   
   traffic_report_temp = []
   for i in range(len(traffic_report)):
      list = []
      for j in range(traffic_report_cols):
         list.append(traffic_report[i][j])
         
      traffic_report_temp.append(list)
      
   
   # #Matched Reports
   # matched_report = db_select("*","UserReports")  
   # matched_report_cols = len(matched_report[0])
   
   # matched_report_temp = []
   # for i in range(len(matched_report)):
   #    list = []
   #    for j in range(matched_report_cols):
   #       list.append(matched_report[i][j])
         
   #    matched_report_temp.append(list)
   
   
   
   #Matched Reports
   matched_report = db_select_where("*","AllRecords", "LicencePlate", "AAA002")  
   matched_report_cols = len(matched_report[0])
   num_matched_report = len(matched_report)

   matched_report_temp = []
   for i in range(len(matched_report)):
      list = []
      for j in range(matched_report_cols):
         list.append(matched_report[i][j])
         
      matched_report_temp.append(list)
   
   print(f"matched_report_temp:::::::::{matched_report_temp}")
   
   return render_template("traffic_report.html", 
                          traffic_report = traffic_report_temp,
                          matched_report = matched_report_temp,
                          num_traffic_report = num_traffic_report,
                          num_matched_report = num_matched_report
                          )


################################################################################################
# Users
################################################################################################
@app.route("/users")
def users():
   
   #Users
   user_records = db_select("*","Users")  
   user_records_cols = len(user_records[0])
   
   user_records_temp = []
   for i in range(len(user_records)):
      list = []
      for j in range(user_records_cols):
         list.append(user_records[i][j])
         
      user_records_temp.append(list)

   
   return render_template("users.html", 
                          user_records = user_records_temp
                          )

################################################################################################
# Cameras
################################################################################################
@app.route("/cameras")
def cameras():
   
   #Cameras
   camera_records = db_select("*","Cameras")  
   camera_records_cols = len(camera_records[0])
   
   camera_records_temp = []
   for i in range(len(camera_records)):
      list = []
      for j in range(camera_records_cols):
         list.append(camera_records[i][j])
         
      camera_records_temp.append(list)
   
   
   return render_template("cameras.html",
                          camera_records = camera_records_temp 
                          )





################################################################################################
# User Form
################################################################################################
@app.route('/user_form', methods=['GET', 'POST'])
def user_form():
   if request.method == 'POST':
      # Get form data
      first_name = request.form['firstName']
      last_name = request.form['lastName']
      email = request.form['email']
      phone = request.form['phone']
      location = request.form['location']
      detail = request.form['detail']
      # Process file uploads
      file = request.files['file']
      if file:
         file.save('uploads/' + file.filename)
      # Optionally process video uploads
      video = request.files['video']
      if video:
         video.save('uploads/' + video.filename)
         
      flash('Your report has been submitted successfully')    
         
   #   return 'Form submitted successfully!'
   
   return render_template('user_form.html')



@app.route("/user_form2")
def user_form2():
    form = UserReportForm()
    
    if request.method == 'POST': 
        if form.validate() == False: 
            flash('All fields are required.') 
            return render_template('register.html', form = form) 
        else: 
            return render_template('index.html') 
    
    if request.method == 'GET': 
        return render_template('register.html', form = form) 



@app.route('/add_account', methods=['POST'])
def add_account(): 
   form = UserRegistrationForm()
   
   if form.validate_on_submit(): 
      
      # Check existing email
      entered_email = form.email.data
      try:
         existing_email = db_select_where("Email", "Users", "Email", entered_email)
         if entered_email in existing_email[0]:
            flash("Your email is already in use. Please sign in instead")
            return render_template('signup.html', form = form)
         
      except:
         db_insert_users(form)
         new_user = db_select_where("*", "users", "Email", form.email.data)
         new_user = load_user(new_user[0][0])
         login_user(new_user)

         return redirect(url_for('success',request = "add_account"))
         # return render_template('index.html')
   else:
      return render_template('signup.html', form = form) 
   


@app.route('/signin_account', methods=['POST'])
def signin_account():
   if request.method == 'POST':   
      entered_email = request.form['email']
      entered_password = request.form['password']

      try:
         registered_user = db_select_where("*","Users", "Email", entered_email)
         registered_password = registered_user[0][5]
         
         
      except:
         registered_user = "None"
         
      if registered_user != "None":
         if check_password(registered_password,entered_password):
            registered_user = load_user(registered_user[0][0])
            login_user(registered_user)
            
            # return redirect(url_for('success', request="signin"))
            # 0. Current user
            current_user_id = str(current_user.get_id())
            user_info = db_select_where("*","Users", "UserID", current_user_id) 
            return render_template('index.html', 
                                   user_info = user_info)
         
         else:
            flash('Your password is wrong')
            return redirect(url_for('login')) 
      else:
         flash('Your email is not registered')
         return redirect(url_for('login')) 
      
      
      

@app.route('/submit_user_report', methods=['POST'])
def submit_user_report(): 
   form = UserReportForm()

   if form.validate_on_submit(): 
      db_insert_user_report(form)

      # return redirect(url_for('dashboard'))
      return render_template('register.html', form = form) 

   return render_template('register.html', form = form) 


################################################################################################
# Account Page
################################################################################################
@app.route("/account")
def account():   
   # 0. Current user
   current_user_id = str(current_user.get_id())
   user_info = db_select_where("*","Users", "UserID", current_user_id)  
   
   return render_template("account.html",
                          user_info = user_info)



################################################################################################
# Success
################################################################################################
# @app.route("/success")
# def success():
   
   
#    title = "Ordered successfully"
#    detail = "Thank you for placing your order!"
         
#    return render_template("success.html", 
#                           title=title, 
#                           detail=detail) 



@app.route("/success/<string:request>")
def success(request):
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   if request == "add_account":
      title = "Added your account successfully"
      detail = "Welcome to " + current_user.FirstName + " " + current_user.LastName
      
   
   
   # elif request == "search_fail":
   #    title = "Item not found"
   #    detail = "Try other search key words"
      
   return render_template("success.html", 
                          title=title, 
                          detail=detail) 



if __name__ == '__main__':
   app.run(debug = True)