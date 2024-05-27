import sqlite3 as sql
# from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import pandas as pd
import datetime

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
    
def db_select_where(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} = '{col_value}'")
        list= cur.fetchall(); 
        return list

def db_select_where_above(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        # cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} > '{col_value}'")
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} > '{col_value}' AND {col_target} != ''")
        list= cur.fetchall(); 
        return list

def db_select_where_above_by_month(col, table, col_target, col_value, month):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        # cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} > '{col_value}'")
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
        cur.execute(f"SELECT {col}, COUNT(id) FROM {table} WHERE status = 'Online' OR status='Offline' GROUP BY {status} ORDER BY 'status' DESC")
        list= cur.fetchall(); 
        return list
    
    
    
    
############################################################
# Insert
############################################################
def db_insert_user_report(form):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        name = form.first_name.data + form.last_name.data
        
        cur.execute("INSERT INTO UserReports (date, location, licencePlate, brand, carType, color, risk, report, user, phone, email, detail) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (date, form.location.data,"LicencePlate","brand","carType","color","risk","report", name,form.phone.data,form.email.data, form.detail.data))
        con.commit()

def db_insert_users(form):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        # Hashing & Salting
        hashed_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        cur.execute("INSERT INTO Users (FirstName, LastName, Phone, Email, Password, Role, Authorized, Status, UserType) VALUES (?,?,?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, "", form.email.data, hashed_salted_password, form.first_name.data, form.first_name.data, form.first_name.data, form.first_name.data))
        con.commit()
        
def db_insert_cars_count(form):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        # cur.execute("INSERT INTO UserReports (FirstName, LastName, Address, Phone, Email, CardNumber, UserType, Password) VALUES (?,?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data, user_type, hashed_salted_password))
        cur.execute("INSERT INTO CarDirection (Area, In, Out, Volume) VALUES (?,?,?,?)",(form.first_name.data, form.first_name.data, form.first_name.data,form.first_name.data))
        con.commit()


def db_insert_cars_detected(object, i):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        # Data list
        # year = object.detected_date[i]
        speed_limit = 100
        detected_speed = object.dist_data[i]
        exceeding_speed_rate = (detected_speed- speed_limit) / speed_limit * 100
        detected_class = object.detected_cars[i]
        detected_direction = object.detected_directions[i]
        
        cur.execute("INSERT INTO AllRecords (Date,Year,Month,Day,Time,DataSource,Location,LicencePlate,Brand,CarType,Color,SpeedLimit,Speed,ExceedingRate,Direction,Video,Image,Status,Detail) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(object.detected_date[i],object.detected_year[i],object.detected_month[i],object.detected_day[i],object.detected_time[i],"Camera","Highway-1","","",detected_class,"",speed_limit, detected_speed,exceeding_speed_rate, detected_direction,"","","",""))
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
        # print(LicencePlate_list)

        #Cars
        Cars_list = db_select("LicencePlate", "Cars")

        #All Records
        All_Record_list = db_select("*", "AllRecords")
        
        #Compare
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

        
        # return new_list

        # cur.execute("INSERT INTO Cars (CarID, LicencePlate, Brand, CarType, Color, Speedings, CarViolation, TrafficReport, Reported, MostUseRoad, Risk) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, "", form.email.data, hashed_salted_password, form.first_name.data, form.first_name.data, form.first_name.data, form.first_name.data))
        # con.commit()


    
# SELECT LicencePlate, COUNT(LicencePlate) FROM AllRecords WHERE LicencePlate = 'AAA002' AND ExceedingRate >10
        
def check_password(registered_password, entered_password):
    return check_password_hash(registered_password, entered_password)