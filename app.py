import mysql.connector
from mysql.connector import Error
# connecting to my mysql
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
# greeting 
print('Welcome to Fast Rentals')
print ('Here to provide fast rentals!')
# function for displaying cars
def get_cars():
    try:
        sql_select_Query = "SELECT * FROM Cars"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        
        print("\n=== Car Records ===")
        
        if cursor.rowcount == 0:
            print("No cars found.")
        else:
            print("Total number of cars: ", cursor.rowcount)
            for row in records:
                print(f"\nCar ID: {row[0]}")
                print(f"  Manufacturer: {row[1]}")
                print(f"  Model: {row[2]}")
                print(f"  Year: {row[3]}")
                print(f"  Price per day: £{row[4]:.2f}")
            
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)    
# function for creating a new car
def create_new_car():
    try:
        manufacturer = input("Enter the manufacturer of the car: ")
        model = input("Enter the model of the car: ")
        year = int(input("Enter the year of the car: "))
        price_per_day = float(input("Enter the price per day of the car: "))

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Cars (Manufacturer, Model, Year, Price_per_day) VALUES (%s, %s, %s, %s)",
                (manufacturer, model, year, price_per_day))
            connection.commit()
            print("Car successfully added to the database.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
# function for updating existing car
def update_car():
    get_cars() 
    try:
        car_to_update = int(input('Select car ID to update: '))
        input_manufacturer = input('Enter the new manufacturer (press Enter to keep current): ')
        input_model = input('Enter the new model (press Enter to keep current): ')
        input_year = input('Enter the new year (press Enter to keep current): ')
        input_price_per_day = input('Enter the new price per day (press Enter to keep current): ')
        
        if input_manufacturer == "" and input_model == "" and input_year == "" and input_price_per_day == "":
            return
        else:
            set_sql_clauses = []
            
            if input_manufacturer != "":
                set_sql_clauses.append(f"Manufacturer = '{input_manufacturer}'")
            
            if input_model != "":
                set_sql_clauses.append(f"Model = '{input_model}'")
            
            if input_year != "":
                set_sql_clauses.append(f"Year = '{input_year}'")
            
            if input_price_per_day != "":
                set_sql_clauses.append(f"Price_per_day = {input_price_per_day}")
                
            set_sql_clause = ", ".join(set_sql_clauses)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Cars SET " + set_sql_clause + " WHERE Car_ID = %s",
                    [car_to_update])
                connection.commit()
                print("Car successfully updated.")
                
    except mysql.connector.Error as e:
        print(f"Error: {e}")       
# function to delete a car
def delete_car():
    get_cars()
    try:
        car_to_delete = int(input('Enter the ID of the car to delete: '))
        
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Cars WHERE Car_ID = %s",
                (car_to_delete,))
            connection.commit()
            print("Car successfully deleted.")
                
    except mysql.connector.Error as e:
        print(f"Error: {e}")
# function for displaying rentals
def get_rentals():
    try:
        while True:
            print("\n=== Rental Orders ===")
            print("0 - Return to Main Menu")
            print("1 - Show all rental orders")
            print("2 - Show rental orders with rented cars")
            
            option = int(input("Select an option: "))
            
            if option == 0:
                return
            elif option == 1:
                sql_select_Query = "SELECT * FROM Rental_Orders"
                cursor = connection.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
            elif option == 2:
                sql_select_Query = """
                SELECT ro.Rental_ID, ro.Renter_Name, c.Car_ID, c.Manufacturer, c.Model, c.Year
                FROM Rental_Orders ro
                LEFT JOIN Rental_Cars rc ON ro.Rental_ID = rc.Rental_ID
                LEFT JOIN Cars c ON rc.Car_ID = c.Car_ID
                """
            
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            
            records = cursor.fetchall()
            
            if cursor.rowcount == 0:
                print("No rental orders found.")
            else:
                print("Total number of rental orders: ", cursor.rowcount)
                for row in records:
                    print(f"\nRental ID: {row[0]}")
                    print(f"  Renter Name: {row[1]}")
                    if option == 1:
                        print(f"  Renter Address: {row[2]}")
                        print(f"  Contact Number: {row[3]}")
                        print(f"  Days Hired: {row[4]}")
                        print(f"  Total Price: £{row[5]:.2f}")
                        print(f"  Hire Date: {row[6]}")
                    elif option == 2:
                        print(f"  Car ID: {row[2]}")
                        print(f"  Manufacturer: {row[3]}")
                        print(f"  Model: {row[4]}")
                        print(f"  Year: {row[5]}")
                
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)
# function for new rental
def add_new_rental():   
    get_cars() 
    try:
        car_id = input("Enter the car ID for the hired car: ")
        renter_name = input("Enter the renter name: ")
        renter_address = input("Enter the renter address: ")
        contact_number = input("Enter the contact number: ")
        days_hired = int(input("Enter the number of days hired: "))
        total_price = float(input("Enter the total price: "))
        hire_date = input("Enter the hire date (YYYY-MM-DD): ")
        
        if not contact_number.isdigit():
            raise ValueError("Contact number should contain only digits.")
        if days_hired <= 0 or total_price <= 0:
            raise ValueError("Days hired and total price should be positive values.")

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Rental_Orders (Renter_Name, Renter_Address, Contact_Number, Days_Hired, Total_Price, Hire_Date) VALUES (%s, %s, %s, %s, %s, %s)",
                (renter_name, renter_address, contact_number, days_hired, total_price, hire_date))
            
            rental_id = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO Rental_Cars (Rental_ID, Car_ID) VALUES (%s, %s)",
                (rental_id, car_id))
            
            connection.commit()
            print("Rental order successfully added to the database.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
# function for updating rental
def update_renter_details():
    get_rentals() 
    try:
        order_to_update = int(input('Select rental order to update: '))
        if order_to_update < 1:
            raise ValueError("Invalid rental order ID. Please enter an existing Rental ID.")
        new_renter_name = input('Enter the new renter name (press Enter to keep current): ')
        new_renter_address = input('Enter the new renter address (press Enter to keep current): ')
        new_contact_number = input('Enter the new renter contact number (press Enter to keep current): ')

        with connection.cursor() as cursor:
            if new_renter_name != "":
                cursor.execute(
                    "UPDATE Rental_Orders SET Renter_Name = %s WHERE Rental_ID = %s",
                    (new_renter_name, order_to_update)
                )
            if new_renter_address != "":
                cursor.execute(
                    "UPDATE Rental_Orders SET Renter_Address = %s WHERE Rental_ID = %s",
                    (new_renter_address, order_to_update)
                )
            if new_contact_number != "":
                cursor.execute(
                    "UPDATE Rental_Orders SET Contact_Number = %s WHERE Rental_ID = %s",
                    (new_contact_number, order_to_update)
                )
            connection.commit()

        print("Rental order successfully updated.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
# function for deleting order 
def delete_rental(): 
    get_rentals()
    try:
        rental_to_delete = int(input('Enter the rental ID to delete: '))
        
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Rental_Orders WHERE Rental_ID = %s",
                (rental_to_delete,)
            )
            connection.commit()

        print(f"Rental with ID {rental_to_delete} is successfully deleted.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
# Define function to print main menu
def print_main_menu():
    print("\n=== Main Menu ===")
    print("0 - Exit App")
    print("1 - Car Menu")
    print("2 - Rental Menu")
# print car menu
def print_car_menu():
    print("\n=== Car Menu ===")
    print("0 - Return to Main Menu")
    print("1 - Show Cars")
    print("2 - Add New Car")
    print("3 - Update Existing Car")
    print("4 - Delete Car")
# print rental menu
def print_rental_menu():
    print("\n=== Rental Menu ===")
    print("0 - Return to Main Menu")
    print("1 - Show Rental Orders")
    print("2 - New Rental")
    print("3 - Update Rental")
    print("4 - Delete Rental")
# App menu
while True:
    # Print main menu
    print_main_menu()
    
    # Select a Main Menu option
    menu_option = int(input('Select a Main Menu option: '))
    
    # Exit App
    if menu_option == 0:
        print("Exiting...")
        break
    
    # Car Menu
    elif menu_option == 1:
        while True:
            # Print car menu
            print_car_menu()
            
            # Car Menu option
            car_menu_option = int(input('Car Menu option: '))
            
            if car_menu_option == 0:
                break
            elif car_menu_option == 1:
                get_cars()
            elif car_menu_option == 2:
                create_new_car()
            elif car_menu_option == 3: 
                update_car()
            elif car_menu_option == 4:
                delete_car()
    
    # Rental Menu      
    elif menu_option == 2:
        while True:
            # Print user menu
            print_rental_menu()
            
            # User Menu option
            rental_menu_option = int(input('User Menu option: ')) 
            
            if rental_menu_option == 0:
                break
            elif rental_menu_option == 1:
                get_rentals()
            elif rental_menu_option == 2:
                add_new_rental()                     
            elif rental_menu_option == 3: 
                update_renter_details()
            elif rental_menu_option == 4:    
                delete_rental()
            
                

                
                
        
