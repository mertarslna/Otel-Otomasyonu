-- Customers Tablosu
INSERT INTO Customers (Age, Gender, Name, Phone, Email)
VALUES 
(30, 'Male', 'John Doe', '5551234567', 'john.doe@example.com'),
(25, 'Female', 'Jane Smith', '5552345678', 'jane.smith@example.com'),
(40, 'Male', 'Michael Brown', '5553456789', 'michael.brown@example.com'),
(35, 'Female', 'Emily Davis', '5554567890', 'emily.davis@example.com'),
(28, 'Male', 'David Wilson', NULL, 'david.wilson@example.com');

-- Reviews Tablosu
INSERT INTO Reviews (Customer_id, Rating, Comments, Comment_Date)
VALUES 
(1, 5, 'Great service and friendly staff!', '2024-12-01'),
(2, 4, 'The room was clean but a bit noisy.', '2024-12-02'),
(3, 3, 'Average experience, nothing special.', '2024-12-03'),
(4, 5, 'Loved the food and the view from my room!', '2024-12-04'),
(5, 2, 'Poor customer service, not recommended.', '2024-12-05');

-- Hotel Tablosu
INSERT INTO Hotel (Hotel_Name, Location, Score)
VALUES 
('Grand Hotel', 'New York, USA', 4.5),
('Ocean View', 'Miami, USA', 4.0),
('Mountain Retreat', 'Denver, USA', 4.7),
('City Inn', 'Chicago, USA', 3.8),
('Sunrise Resort', 'Orlando, USA', 4.2);

-- Rooms Tablosu
INSERT INTO Rooms (Hotel_id, Room_Type, Price, Available)
VALUES 
(1, 'Deluxe Suite', 200.00, 1),
(2, 'Single Room', 100.00, 1),
(3, 'Double Room', 150.00, 0),
(4, 'Family Room', 180.00, 1),
(5, 'Penthouse', 300.00, 1);

-- Bills Tablosu
INSERT INTO Bills (Customer_id, Date, Amount)
VALUES 
(1, '2024-12-06', 250.00),
(2, '2024-12-07', 150.00),
(3, '2024-12-08', 300.00),
(4, '2024-12-09', 400.00),
(5, '2024-12-10', 200.00);

-- Reservations Tablosu
INSERT INTO Reservations (Customer_id, Room_Number, Start_Date, End_Date)
VALUES 
(1, 1, '2024-12-15', '2024-12-20'),
(2, 2, '2024-12-16', '2024-12-18'),
(3, 3, '2024-12-17', '2024-12-19'),
(4, 4, '2024-12-18', '2024-12-22'),
(5, 5, '2024-12-19', '2024-12-25');

-- Admins Tablosu
INSERT INTO Admins (Admin_Name, Username, Password)
VALUES 
('Mert', '1', '1'),
('Yusuf', 'ysf', '1453'),
('Admin1', 'admin1', 'securepass'),
('Admin2', 'admin2', 'mypassword'),
('Admin3', 'admin3', '123456');
