import pymysql
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
host_name = os.environ.get("mysql_host")
database_name = os.environ.get("mysql_db")
user_name = os.environ.get("mysql_user")
user_password = os.environ.get("mysql_pass")


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='fast_rentals',
                                         user='root',
                                         password='password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        
except Error as e:
    print("Error while connecting to MySQL", e)

try:
    mySql_Create_Table_Query = """CREATE TABLE Cars ( 
                             Car_ID int(11) NOT NULL AUTO_INCREMENT,
                             Manufacturer varchar(250) NOT NULL,
                             Model varchar(250) NOT NULL,
                             Year int(11) NOT NULL,
                             Price_per_day float NOT NULL,
                             PRIMARY KEY (Car_ID)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Cars Table created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
    
try:
    mySql_insert_query = """INSERT INTO Cars (Manufacturer, Model, Year, Price_per_day) 
                           VALUES (%s, %s, %s, %s)"""
    records_to_insert = [('Toyota', 'Camry', 2022, 75.0),
                       ('Ford', 'Mustang', 2021, 95.0),
                       ('Honda', 'Civic', 2022, 70.5),
                       ('Volkswagon', 'Golf R', 2021, 83.0),
                       ('Tesla', 'Model S', 2021, 100.0),
                       ('Nissan', 'Altima', 2020, 65.5),
                       ('BMW', 'X5', 2022, 120.0),
                       ('Mercedes', 'C-Class', 2021, 110.0),
                       ('Audi', 'A4', 2022, 100.0),
                       ('Hyundai', 'Elantra', 2021, 62.0)]
                       

    cursor = connection.cursor()
    cursor.executemany(mySql_insert_query, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Cars table")
    cursor.close()

except mysql.connector.Error as error:
   print("Failed to insert records into Cars table {}".format(error))
        
    
    
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='fast_rentals',
                                         user='root',
                                         password='password')

    mySql_Create_Table_Query = """CREATE TABLE Rental_Orders ( 
                             Rental_ID int(11) NOT NULL AUTO_INCREMENT,
                             Renter_Name varchar(250) NOT NULL,
                             Renter_Address varchar(250) NOT NULL,
                             Contact_Number varchar(20) NOT NULL,
                             Days_Hired int(11) NOT NULL,
                             Total_Price float NOT NULL,
                             Hire_Date varchar(250) NOT NULL,
                             PRIMARY KEY (Rental_ID)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Rental Orders Table created successfully ")
    
except mysql.connector.Error as error:
    print("Failed to create Rental Orders table:", error)
    
try:
    orders_to_insert = """INSERT INTO Rental_Orders (Renter_Name, Renter_Address, Contact_Number, Days_Hired, Total_Price, Hire_Date) 
                           VALUES (%s, %s, %s, %s, %s, %s)"""
                           
    rental_data = [
        ('John Doe', '123 Main St, Anytown, AB123CD', '+441234567890', 5, 600.0, '2024-03-16'),
        ('Jane Smith', '456 Elm St, Othertown, EF456GH', '+447700123456', 3, 186.0, '2024-03-17'),
        ('Alice Johnson', '789 Oak St, Anothertown, IJ789KL', '+445555555555', 7, 581.0, '2024-03-18'),
        ('Bob Brown', '101 Pine St, Yetanothertown, MN101OP', '+447777777777', 2, 200.0, '2024-03-19')
    ] 

    cursor = connection.cursor()
    cursor.executemany(orders_to_insert, rental_data)
    connection.commit()
    print(cursor.rowcount, "Record(s) inserted successfully into Rental Orders table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into Rental Orders table:", error)
    
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='fast_rentals',
                                         user='root',
                                         password='password')

    mySql_Create_Table_Query = """ CREATE TABLE IF NOT EXISTS Rental_Cars (
                    Rental_ID INT NOT NULL,
                    Car_ID INT NOT NULL,
                    FOREIGN KEY (Rental_ID) REFERENCES Rental_Orders(Rental_ID),
                    FOREIGN KEY (Car_ID) REFERENCES Cars(Car_ID))"""
        
    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Rental Cars Table created successfully ")
    
except mysql.connector.Error as error:
    print("Failed to create Rental Cars table:", error)
    
try:
    orders_to_insert = """INSERT INTO Rental_Cars (Rental_ID, Car_ID) 
                           VALUES (%s, %s)"""
                           
    rental_cars_data = [
        (1, 5),
        (2, 10),
        (3, 4),
        (4, 9)
    ] 

    cursor = connection.cursor()
    cursor.executemany(orders_to_insert, rental_cars_data)
    connection.commit()
    print(cursor.rowcount, "Record(s) inserted successfully into Rental Cars table")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into Rental Cars table:", error)