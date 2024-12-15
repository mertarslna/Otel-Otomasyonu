CREATE TABLE Customers (
    Customer_id INT IDENTITY(1,1) PRIMARY KEY,
    Age INT NOT NULL,
    Gender NVARCHAR(10) NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    Phone NVARCHAR(20) NULL,
    Email NVARCHAR(100) NULL
);

CREATE TABLE Reviews (
    Review_id INT IDENTITY(1,1) PRIMARY KEY,
    Customer_id INT NOT NULL,
    Rating INT NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
    Comments NVARCHAR(MAX) NULL,
    Comment_Date DATE NOT NULL,
    FOREIGN KEY (Customer_id) REFERENCES Customers(Customer_id)
);

CREATE TABLE Hotels (
    Hotel_id INT IDENTITY(1,1) PRIMARY KEY,
    Hotel_Name VARCHAR(100),
    Location VARCHAR(200),
    Score DECIMAL(3, 2)
);

CREATE TABLE Rooms (
    Room_id INT IDENTITY(1,1) PRIMARY KEY,
    Hotel_id INT NOT NULL,
    Room_Type NVARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Available BIT NOT NULL DEFAULT 1
);

CREATE TABLE Bills (
    Bill_id INT IDENTITY(1,1) PRIMARY KEY,
    Customer_id INT NOT NULL,
    Date DATE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Customer_id) REFERENCES Customers(Customer_id)
);

CREATE TABLE Reservations (
    Reservation_id INT IDENTITY(1,1) PRIMARY KEY,
    Customer_id INT NOT NULL,
    Room_Number INT NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    FOREIGN KEY (Customer_id) REFERENCES Customers(Customer_id),
    FOREIGN KEY (Room_Number) REFERENCES Rooms(Room_id)
);

CREATE TABLE Admins (
    Admin_id INT IDENTITY(1,1) PRIMARY KEY,
    Admin_Name NVARCHAR(100) NOT NULL,
    Username NVARCHAR(50) NOT NULL,
    Password NVARCHAR(255) NOT NULL
);
