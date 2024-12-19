CREATE DATABASE Hotel;

CREATE TABLE Guests(
	Guest_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(20) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Phone INT NOT NULL UNIQUE
);
CREATE TABLE Rooms(
	Room_ID INT PRIMARY KEY AUTO_INCREMENT,
    Room_number INT NOT NULL UNIQUE,
    Room_Type VARCHAR(20) NOT NULL,
    available bool default 1,
    cost float,
    Rate Float DEFAULT 0
);
CREATE TABLE Reservations(
	Reservation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Check_in DATE DEFAULT current_timestamp,
    Check_out DATE,
    Bill FLOAT,
    Guest_ID INT,
    Room_ID INT,
    FOREIGN KEY(Guest_ID) REFERENCES Guests(Guest_ID),
    FOREIGN KEY(Room_ID) REFERENCES Rooms(Room_ID)
)