from flask import Flask, render_template, Response,jsonify,request,session, flash, redirect, url_for
from flask_wtf import FlaskForm
from forms import UserReportForm, UserRegistrationForm, UserLoginForm, SearchForm, OperatorReportForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
# from auto_report import send_email2
import os
from datetime import timedelta
import datetime
from db_handler import db_select, db_select_where, db_select_count_data_by_day, db_select_count_speedings_by_day, db_select_count_camera_by_status, db_insert_user_report, db_insert_users, check_password, db_select_where_above_by_month, db_update_cars, db_select_order, db_insert_user_report

# Required to run the YOLOv8 model
import cv2
# Video Detection for Object Detection on Input Video
from YOLO_Video import video_detection
from predict import predict


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


# FlaskForm to get input video file  from user
class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")

# Generate frames for upload
def generate_frames(path_x = ''):
   yolo_output = predict(path_x)
   for detection_ in yolo_output:
      ref,buffer=cv2.imencode('.jpg',detection_)

      frame = buffer.tobytes()
      yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')

# Generate frames for real-time (live video)
def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)
        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')


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
@app.route("/signup", methods=['GET', 'POST'])
def signup():
   form = UserRegistrationForm()
    
   if request.method == 'POST': 
      if form.validate_on_submit(): 
         
         # Check existing email
         entered_email = form.email.data
         try:
            existing_email = db_select_where("Email", "Users", "Email", entered_email)
            if entered_email in existing_email[0]:
               # email exists
               flash("Your email is already in use. Please sign in instead")
               return render_template('signup.html', form = form)
            
         except:
            # success
            db_insert_users(form)
            new_user = db_select_where("*", "users", "Email", form.email.data)
            new_user = load_user(new_user[0][0])
            login_user(new_user)

            return redirect(url_for('success',request = "signup"))

      else:
         # Not filled in
         flash('All fields are required.') 
         return render_template('signup.html', form = form) 
   
   if request.method == 'GET': 
      return render_template('signup.html', form = form) 

################################################################################################
# Signin
################################################################################################
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    if request.method == 'POST': 
      entered_email = request.form['email']
      entered_password = request.form['password']

      try:
         registered_user = db_select_where("*","Users", "Email", entered_email)
         registered_password = registered_user[0][5]
      except:
         registered_user = "None"
         
      if registered_user != "None":
         # success
         if check_password(registered_password,entered_password):
            registered_user = load_user(registered_user[0][0])
            login_user(registered_user)
            
            current_user_id = str(current_user.get_id())
            user_info = db_select_where("*","Users", "UserID", current_user_id) 
            return redirect(url_for('success', request="signin"))
            # return render_template('dashboard.html', user_info = user_info)
         
         else:
            # password error
            flash('Your password is wrong')
            return redirect(url_for('signin')) 
      else:
         # email error
         flash('Your email is not registered')
         return redirect(url_for('signin')) 
    
   
    if request.method == 'GET': 
        return render_template('signin.html', form = form) 


################################################################################################
# Sign out
################################################################################################
@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('landing'))

################################################################################################
# Dashbords
################################################################################################
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   user_info = db_select_where("*","Users", "UserID", current_user_id)  
   
   # Current Month
   current_month = datetime.datetime.now().strftime("%-m")
   selected_month = current_month
   
   if request.method == 'POST':
      selected_month = request.form['mySelect']
   
   # 1. All Records
   all_records = db_select("*","AllRecords")

   # 2. Number of cars by month
   car_list = db_select_where("*","AllRecords", "Month", selected_month)  
   num_cars = (len(car_list))
   
   # 3. Number of exceeding cars
   exceeding_rate = db_select_where_above_by_month("*","AllRecords", "ExceedingRate", 20, selected_month)
   num_exceedings = len(exceeding_rate)
   
   
   #the number of data by days
   dayly_count_list = db_select_count_data_by_day("Day","AllRecords", selected_month)  
   
   data1 = [['Date', 'Count']]
   for i in range(len(dayly_count_list)):
      list = []
      list.append(dayly_count_list[i][0])
      list.append(dayly_count_list[i][1])
      data1.append(list)
      
      
   #the number of data by speedings and days
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

   
   return render_template("dashboard.html", 
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
   return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')
   

################################################################################################
# All Records
################################################################################################
@app.route("/allrecords")
def allrecords():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
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
                          all_records = all_records_temp,
                          current_user_id = current_user_id
                          )

################################################################################################
# Cars
################################################################################################
@app.route("/cars")
def cars():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
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
                          car_records = car_records_temp,
                          current_user_id = current_user_id
                          )

################################################################################################
# Map
################################################################################################
@app.route("/map")
def map():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   return render_template("map.html", 
                          current_user_id = current_user_id
                          )
   
################################################################################################
# Analysis
################################################################################################
@app.route('/analysis', methods=['GET','POST'])
def analysis():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
   # Upload File Form
   form = UploadFileForm()
   
   if form.validate_on_submit():
      # uploaded video file path is saved here
      file = form.file.data
      file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                              secure_filename(file.filename)))  
      # session storage to save video file path
      session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                          secure_filename(file.filename))
   
   return render_template('analysis.html', 
                          form=form,
                          current_user_id = current_user_id
                          )

################################################################################################
# Video
################################################################################################
@app.route('/video')
def video():
   return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')
 

################################################################################################
# Traffic Report
################################################################################################
@app.route("/trafficreport", methods=['GET','POST'])
def trafficreport():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
   #Traffic Report
   traffic_report = db_select_order("*","UserReports", "Date", "DESC")  
   traffic_report_cols = len(traffic_report[0])
   num_traffic_report = len(traffic_report)
   
   traffic_report_temp = []
   for i in range(len(traffic_report)):
      list = []
      for j in range(traffic_report_cols):
         list.append(traffic_report[i][j])
         
      traffic_report_temp.append(list)
   
   # # Get form data
   # form1 = SearchForm()
   # form2 = OperatorReportForm()
   
   if request.method == 'GET':
      plateNumber = ''
      reported_image_name = "user_report.png"
      reported_video_name = "user_report.png"
      matched_image_name = "searched_result.png"
      matched_video_name = "searched_result.png"
      
   if request.method == 'POST':
      # Check the selected image and video names
      try:
         plateNumber = request.form['plateNumber']
         reported_image_name = request.form['reportedImageName']
         reported_video_name = request.form['reportedVideoName']
         matched_image_name = db_select_where("Image","AllRecords", "LicencePlate", plateNumber)[0][0]
         matched_video_name = db_select_where("Video","AllRecords", "LicencePlate", plateNumber)[0][0]
      except:
         # plateNumber = ""
         plateNumber2 = request.form['plateNumber2']
         return redirect(url_for('success',request = "operator_report"))
         
      #Matched Reports
      matched_report = db_select_where("*","AllRecords", "LicencePlate", plateNumber) 
      if matched_report:
         matched_report_cols = len(matched_report[0])
         num_matched_report = len(matched_report)
      else:
         matched_report_cols = 0
         num_matched_report = 0
         flash('No result') 
      
      matched_report_temp = []
      for i in range(len(matched_report)):
         list = []
         for j in range(matched_report_cols):
            list.append(matched_report[i][j])
            
         matched_report_temp.append(list)
   
      return render_template("traffic_report.html", 
                           traffic_report = traffic_report_temp,
                           matched_report = matched_report_temp,
                           num_traffic_report = num_traffic_report,
                           num_matched_report = num_matched_report,
                           reported_image_name = reported_image_name,
                           reported_video_name = reported_video_name,
                           matched_image_name = matched_image_name,
                           matched_video_name = matched_video_name,
                           current_user_id = current_user_id
                           )
      
   
   return render_template("traffic_report.html",
                          traffic_report = traffic_report_temp,
                          num_traffic_report = num_traffic_report,
                          reported_image_name = reported_image_name,
                          reported_video_name = reported_video_name,
                          matched_image_name = matched_image_name,
                          matched_video_name = matched_video_name,
                          current_user_id = current_user_id
                           )


################################################################################################
# Users
################################################################################################
@app.route("/users")
def users():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
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
                          user_records = user_records_temp,
                          current_user_id = current_user_id
                          )

################################################################################################
# Cameras
################################################################################################
@app.route("/cameras")
def cameras():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
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
                          camera_records = camera_records_temp,
                          current_user_id = current_user_id
                          )





################################################################################################
# User Form
################################################################################################
@app.route("/user_report", methods=['GET', 'POST'])
def user_report():
   form = UserReportForm()
   
   if request.method == 'POST': 
      if form.validate_on_submit(): 
         image = form.image.data
         if(image == None):
            image_name = "-"
         else:
            # Extract only the file name
            image_name = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
            

         video = form.video.data
         if(video == None):
            video_name = "-"
         else:
            # Extract only the file name
            video_name = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_name))
            
         # Check plate number
         plate_number = form.plate_number.data
         location = form.location.data
         car_type = form.car_type.data
         
         try:
            # Check risk level of the car
            risk_level = db_select_where("Risk", "Cars", "LicencePlate", plate_number)[0][0]
            
            if "High" in risk_level or "Mid" in risk_level:
               report_status = "Reported"
               # Send email
               # send_email2(risk_level, location, car_type, plate_number)
            else:
               risk_level = "Low"
               report_status = "-"
         except:
            risk_level = "-"
            report_status = "-"
         
         db_insert_user_report(form, image_name, video_name, risk_level, report_status)
         return redirect(url_for('success',request = "user_report"))
         
   if request.method == 'GET': 
      return render_template('user_report.html', form = form) 


################################################################################################
# Account Page
################################################################################################
@app.route("/account")
def account():   
   # 0. Current user
   current_user_id = str(current_user.get_id())
   user_info = db_select_where("*","Users", "UserID", current_user_id)  
   
   return render_template("account.html",
                          user_info = user_info,
                          current_user_id = current_user_id
                          )

################################################################################################
# Success
################################################################################################
@app.route("/success/<string:request>")
def success(request):
   form = UserReportForm()
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   if request == "signup":
      title = "Added your account successfully"
      detail = "Welcome to " + current_user.FirstName + " " + current_user.LastName
   
   elif request == "signin":
      title = "Sign in successfully"
      detail = "Welcome back " + current_user.FirstName + " " + current_user.LastName
      
   elif request == "user_report":
      title = "Your report has been submitted successfully"
      detail = "Thank you for your cooperation!"
      return render_template("success_user_report.html", 
                        title=title, 
                        detail=detail) 
      
   elif request == "operator_report":
      title = "Your report has been submitted successfully"
      detail = "Thank you for your cooperation!"
      
   return render_template("success.html", 
                          title=title, 
                          detail=detail) 


if __name__ == '__main__':
   app.run(debug = True)