Create Database Hotel;

USE Hotel;

CREATE TABLE Guests(
	Guest_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name text NOT NULL,
	Phone INT NOT NULL,
    Email text NOT NULL
);
CREATE TABLE Rooms(
	Room_Number INT PRIMARY KEY AUTO_INCREMENT,
    Room_Type text NOT NULL,
    Available bool default 1,
    Rate Float DEFAULT 0,
    Price INT NOT NULL
);
CREATE TABLE Services(
	Service_ID INT PRIMARY KEY AUTO_INCREMENT,
    Room_Number INT,
    Name Text,
    Cost float,
    FOREIGN KEY(Room_Number) REFERENCES Rooms(Room_Number)
);
CREATE TABLE Billings(
	Billing_ID INT PRIMARY KEY AUTO_INCREMENT,
    Amount float,
    Date date
);
CREATE TABLE Bookings(
	Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
	Guest_ID INT,
    Room_Number INT,
    Billing_ID INT,
    Check_in DATE NOT NULL,
    Check_out DATE NOT NULL,
    FOREIGN KEY(Guest_ID) REFERENCES Guests(Guest_ID),
    FOREIGN KEY(Room_Number) REFERENCES Rooms(Room_Number),
    FOREIGN KEY(Billing_ID) REFERENCES Billings(Billing_ID)
);
