use fast_rentals;

CREATE TABLE Cars ( 
    Car_ID int(11) NOT NULL AUTO_INCREMENT,
    Manufacturer varchar(250) NOT NULL,
    Model varchar(250) NOT NULL,
    Year int(11) NOT NULL,
    Price_per_day float NOT NULL,
    PRIMARY KEY (Car_ID)
);
   
INSERT INTO Cars (Manufacturer, Model, Year, Price_per_day) 
    VALUES ('Toyota', 'Camry', 2022, 75.0),
    ('Ford', 'Mustang', 2021, 95.0),
    ('Honda', 'Civic', 2022, 70.5),
    ('Volkswagon', 'Golf R', 2021, 83.0),
    ('Tesla', 'Model S', 2021, 100.0),
    ('Nissan', 'Altima', 2020, 65.5),
    ('BMW', 'X5', 2022, 120.0),
    ('Mercedes', 'C-Class', 2021, 110.0),
    ('Audi', 'A4', 2022, 100.0),
    ('Hyundai', 'Elantra', 2021, 62.0);
                       
    CREATE TABLE Rental_Orders ( 
        Rental_ID int(11) NOT NULL AUTO_INCREMENT,
        Renter_Name varchar(250) NOT NULL,
        Renter_Address varchar(250) NOT NULL,
        Contact_Number varchar(20) NOT NULL,
        Days_Hired int(11) NOT NULL,
        Total_Price float NOT NULL,
        Hire_Date varchar(250) NOT NULL,
        PRIMARY KEY (Rental_ID)
    );

 INSERT INTO Rental_Orders (Renter_Name, Renter_Address, Contact_Number, Days_Hired, Total_Price, Hire_Date) 
    VALUES ('John Doe', '123 Main St, Anytown, AB123CD', '+441234567890', 5, 600.0, '2024-03-16'),
        ('Jane Smith', '456 Elm St, Othertown, EF456GH', '+447700123456', 3, 186.0, '2024-03-17'),
        ('Alice Johnson', '789 Oak St, Anothertown, IJ789KL', '+445555555555', 7, 581.0, '2024-03-18'),
        ('Bob Brown', '101 Pine St, Yetanothertown, MN101OP', '+447777777777', 2, 200.0, '2024-03-19');
    
 CREATE TABLE IF NOT EXISTS Rental_Cars (
    Rental_ID INT NOT NULL,
    Car_ID INT NOT NULL,
    FOREIGN KEY (Rental_ID) REFERENCES Rental_Orders(Rental_ID),
    FOREIGN KEY (Car_ID) REFERENCES Cars(Car_ID)
);
        
    
INSERT INTO Rental_Cars (Rental_ID, Car_ID) 
    VALUES (1, 5),
    (2, 10),
    (3, 4),
    (4, 9);
