CREATE TABLE Customer (
    Customer_id INT PRIMARY KEY,
    Age INT,
    Gender VARCHAR(10),
    Name VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Hotel (
    Hotel_id INT PRIMARY KEY,
    Hotel_Name VARCHAR(100),
    Location VARCHAR(200),
    Score DECIMAL(3, 2)
);

CREATE TABLE Room (
    Room_id INT PRIMARY KEY,
    Hotel_id INT,
    Room_Type VARCHAR(50),
    Price DECIMAL(10, 2),
    Available BIT,  -- BOOLEAN yerine BIT kullanýldý
    FOREIGN KEY (Hotel_id) REFERENCES Hotel(Hotel_id)
);

CREATE TABLE Bill (
    Bill_id INT PRIMARY KEY,
    Customer_id INT,
    Date DATE,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
);

CREATE TABLE Reservation (
    Reservation_id INT PRIMARY KEY,
    Customer_id INT,
    Room_Number INT,
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (Room_Number) REFERENCES Room(Room_id)
);

CREATE TABLE Admin (
    Admin_id INT PRIMARY KEY,
    Admin_name VARCHAR(100),
    Username VARCHAR(50),
    Password VARCHAR(100)
);
