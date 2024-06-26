import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import datetime
from flask import request

################################################################################################
# DB Path
################################################################################################
DB_path = 'traffic.db'

################################################################################################
# Functions
################################################################################################
def db_select(col, table):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table}") 
        list= cur.fetchall(); 
        return list

def db_select_order(col, table, order_col, order):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} ORDER BY {order_col} {order}") 
        list= cur.fetchall(); 
        return list
 
def db_select_where(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} = '{col_value}'")
        list= cur.fetchall(); 
        return list

def db_select_where_above(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} > '{col_value}' AND {col_target} != ''")
        list= cur.fetchall(); 
        return list

def db_select_where_above_by_month(col, table, col_target, col_value, month):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} > '{col_value}' AND Month = {month} ")
        list= cur.fetchall(); 
        return list

def db_select_count_data_by_day(col, table, month):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col}, COUNT(CarID) FROM {table} WHERE Month = {month} GROUP BY Year, Month, Day")
        list= cur.fetchall(); 
        return list

def db_select_count_speedings_by_day(col, table, month):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col}, COUNT(CarID) FROM {table} WHERE ExceedingRate > 20 AND Month = {month} GROUP BY Year, Month, Day")
        list= cur.fetchall(); 
        return list
    
def db_select_count_speedings_by_car(col, table, licence_plate):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col}, COUNT(CarID) FROM {table} WHERE ExceedingRate > 20 AND LicencePlate = '{licence_plate}'")
        list= cur.fetchall(); 
        return list
    
def db_select_count_report_by_car(col, table, licence_plate):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col}, COUNT(CarID) FROM {table} WHERE Status = 'Reported' AND LicencePlate = '{licence_plate}'")
        list= cur.fetchall(); 
        return list

def db_select_count_camera_by_status(col, table, status):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col}, COUNT(CameraID) FROM {table} WHERE Status = 'Online' OR Status='Offline' GROUP BY {status} ORDER BY 'Status' DESC")
        list= cur.fetchall(); 
        return list

def db_insert_users(form):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        # Hashing & Salting
        hashed_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        cur.execute("INSERT INTO Users (FirstName, LastName, Phone, Email, Password, Role, Authorized, Status, UserType) VALUES (?,?,?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, "000-000-0000", form.email.data, hashed_salted_password, "Operator", "Yes", "Online", "-"))
        con.commit()
        
def db_insert_cars_count(form):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO CarDirection (Area, In, Out, Volume) VALUES (?,?,?,?)",(form.first_name.data, form.first_name.data, form.first_name.data,form.first_name.data))
        con.commit()

def db_insert_cars_detected(object, i):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        speed_limit = 100
        detected_speed = object.dist_data[i]
        exceeding_speed_rate = (detected_speed- speed_limit) / speed_limit * 100
        detected_direction = object.detected_directions[i]
        data_source = "camera"
        
        # location
        location_list = ["Highway-1", "Highway-2", "Highway-3", "Highway-4", "Highway-5", "Highway-6", "Highway-7"]
        location = random.choice(location_list)
        
        car_id = len(db_select("RecordID", "allRecords"))+1
        
        # licence plate
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        licence_plate = letters + "-" + digits
        
        # brand list
        brand_list = ["Toyota", "Honda", "Nissan", "BMW", "Audi", "Tesla", "BYD"]
        brand = random.choice(brand_list)
        
        # car type
        car_type_list = ["Sedan", "SUV", "Sport", "Compact", "Coupe"]
        car_type = random.choice(car_type_list)
        
        # color
        car_color_list = ["Black", "White", "Red", "Blue", "Yellow", "Green", "Grey"]
        car_color = random.choice(car_color_list)
        
        cur.execute("INSERT INTO AllRecords (CarId, Date,Year,Month,Day,Time,DataSource,Location,LicencePlate,Brand,CarType,Color,SpeedLimit,Speed,ExceedingRate,Direction,Video,Image,Status,Detail) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(car_id, object.detected_date[i],object.detected_year[i],object.detected_month[i],object.detected_day[i],object.detected_time[i],data_source,location,licence_plate, brand, car_type, car_color, speed_limit, detected_speed,exceeding_speed_rate, detected_direction,"","","",""))
        con.commit()

def db_insert_user_report(form, image_name, video_name, risk_level, report_status):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        
        # location
        location_list = ["Highway-1", "Highway-2", "Highway-3", "Highway-4", "Highway-5", "Highway-6", "Highway-7"]
        location = random.choice(location_list)
        
        # plate number
        plate_number = form.plate_number.data
        
        # brand list
        brand_list = ["Toyota", "Honda", "Nissan", "BMW", "Audi", "Tesla", "BYD"]
        brand = random.choice(brand_list)
        
        # car type
        car_type = form.car_type.data
        
        # color
        car_color_list = ["Black", "White", "Red", "Blue", "Yellow", "Green", "Grey"]
        car_color = random.choice(car_color_list)
        
        # risk
        risk = risk_level
        
        # report status
        report = report_status
        
        # user info
        user = form.first_name.data + " " + form.last_name.data
        phone = form.phone.data
        email = form.email.data
        detail = form.detail.data
        
        # image & video
        image = image_name
        video = video_name

        cur.execute("INSERT INTO UserReports (Date, Location, LicencePlate, Brand, CarType, Color, Risk, Report, User, Phone, Email, Detail, Image, Video) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date, location, plate_number, brand, car_type, car_color, risk, report, user, phone, email, detail, image, video))
        con.commit()

def db_update_cars():
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        table_name = "AllRecords"
        cur.execute(f"PRAGMA table_info('{table_name}')") 
        table_info= cur.fetchall(); 

        #LicencePlate Records
        LicencePlate_list = db_select("LicencePlate", "AllRecords")
        LicencePlate_list = list(set(LicencePlate_list))

        #Cars
        Cars_list = db_select("LicencePlate", "Cars")

        #All Records
        All_Record_list = db_select("*", "AllRecords")
        
        #Compare between cars in AllRecords and cars in Cars list
        for i in range(len(LicencePlate_list)):
            if LicencePlate_list[i] in Cars_list:
                pass
            else:
                LicencePlate = db_select_where("LicencePlate", "AllRecords", "LicencePlate", LicencePlate_list[i][0])
                Brand = db_select_where("Brand", "AllRecords", "LicencePlate", LicencePlate_list[i][0])
                CarType = db_select_where("CarType", "AllRecords", "LicencePlate", LicencePlate_list[i][0])
                Color = db_select_where("Color", "AllRecords", "LicencePlate", LicencePlate_list[i][0])
                Speedings = db_select_count_speedings_by_car("LicencePlate", "AllRecords", LicencePlate_list[i][0])
                Violation = random.randint(1, 5)
                TrafficReport = db_select_count_report_by_car("LicencePlate", "AllRecords", LicencePlate_list[i][0])
                MostUseRoad = "Highway-1"
                num_risks = Speedings[0][1] + Violation + TrafficReport[0][1]
                if num_risks >= 5:
                    Risk = "High"
                elif num_risks < 5 and num_risks >= 3:
                    Risk = "Mid"
                else:
                    Risk = "Low"
            
                cur.execute("INSERT INTO Cars (LicencePlate, Brand, CarType, Color, Speedings, CarViolation, TrafficReport, Reported, MostUseRoad, Risk) VALUES (?,?,?,?,?,?,?,?,?,?)",(LicencePlate[0][0],Brand[0][0],CarType[0][0],Color[0][0],Speedings[0][1],Violation ,TrafficReport[0][1],1, MostUseRoad,Risk))
                con.commit()

def db_update_user_info(form, user_id):
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      cur.execute("UPDATE Users SET FirstName=?, LastName=?, Address=?, Phone=?, Email=?, CardNumber=? WHERE UserID=?", (form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data, user_id)) 
      cur.execute("UPDATE Users SET FirstName=? WHERE UserID=?", (form.first_name.data, user_id)) 
      con.commit()
      
def db_delete(table, col_target, col_value):
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute(f"DELETE FROM {table} WHERE {col_target} = '{col_value}'")
      con.commit() 
       
def check_password(registered_password, entered_password):
    return check_password_hash(registered_password, entered_password)


