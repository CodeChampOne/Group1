USE roundspheres;
-- Create Locations Table
CREATE TABLE locations (
    `Location_ID` INT NOT NULL AUTO_INCREMENT, 
   `Location` VARCHAR(100) NOT NULL, 
    `Coordinates` VARCHAR(200), 
    PRIMARY KEY (`Location_ID`)
);
-- Insert Locations
INSERT INTO locations (`Location`, `Coordinates`) 
VALUES ('New York', '40.7128,-74.0060'), ('San Francisco', '37.7749,-122.4194');


-- Create Devices Table
CREATE TABLE devices (
    `Device_ID` INT NOT NULL AUTO_INCREMENT, 
    `Location_ID` INT, 
    `Sphere_Name` VARCHAR(100) NOT NULL, 
    `Sphere_Address` VARCHAR(200), 
    PRIMARY KEY (`Device_ID`), 
    FOREIGN KEY (`Location_ID`) REFERENCES locations(`Location_ID`) ON DELETE SET NULL ON UPDATE CASCADE
);
-- Insert Devices
INSERT INTO devices (`Location_ID`, `Sphere_Name`, `Sphere_Address`) 
VALUES (1, 'Device A', '123 Main St'), (2, 'Device B', '456 Market St');

-- Create Observations Table
CREATE TABLE observations (
    `id` INT NOT NULL AUTO_INCREMENT, 
    `Device_ID` INT, 
    `Location_ID` INT, 
    `Date` DATE NOT NULL, 
    `Time` TIME NOT NULL, 
    `Time_Zone` VARCHAR(10) NOT NULL, 
    `Temperature` FLOAT NOT NULL, 
    `Location` VARCHAR(200), 
    `Humidity` FLOAT, 
    `Wind_Direction` FLOAT, 
    `Precipitation` FLOAT, 
    `Haze` VARCHAR(255), 
    `Status` VARCHAR(100), 
    PRIMARY KEY (`id`), 
    FOREIGN KEY (`Device_ID`) REFERENCES devices(`Device_ID`) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (`Location_ID`) REFERENCES locations(`Location_ID`) ON DELETE CASCADE ON UPDATE CASCADE
);
-- Insert Observations
INSERT INTO observations (`Device_ID`, `Location_ID`, `Date`, `Time`, `Time_Zone`, `Temperature`, `Location`, `Humidity`, `Wind_Direction`, `Precipitation`, `Haze`, `Status`) 
VALUES (1, 1, '2024-01-01', '10:00:00', 'UTC-05:00', 25.0, 'Indoors', 50.0, 180.0, 0.0, 'Clear skies', 'Active');




