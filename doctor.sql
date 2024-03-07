create database hospital;
use hospital;

CREATE TABLE Doctor(
doctor_id int primary key,
doctor_name varchar(50) NOT NULL,
department_id varchar(20) not NULL references department(dept_id),
email varchar(50) NOT NULL,
gender varchar(20) NOT NULL,
password varchar(30) NOT NULL
);

CREATE TABLE Schedule(
id int NOT NULL references Doctor(doctor_id),
starttime TIME NOT NULL,
endtime TIME NOT NULL,
breaktime TIME NOT NULL,
day varchar(20) NOT NULL,
PRIMARY KEY (id, starttime, endtime, breaktime, day)
);

create table Department(
dept_id int primary key,
dept_name varchar(20) not null
);

desc Doctor;
desc Schedule;
desc Department;
desc Staff;
desc Patient;
desc MedicalHistory;
desc Appointment;
desc Diagnose;
desc patientfillhistory;

create table Staff(
staff_id int primary key,
staff_name varchar(20) not null,
designation varchar(20) not null,
availability varchar(10) not null
);

create table Patient( 
name varchar(20) NOT NULL, 
addr varchar(20) NOT NULL, 
gender char(1) NOT NULL, 
email varchar(20) NOT NULL primary key, 
password varchar(20) NOT NULL
);

create table Patientlist( 
doctor_id int NOT NULL,
p_name varchar(20) NOT NULL, 
p_email varchar(20) NOT NULL,
prev_doc varchar(20) NOT NULL,
date DATE, 
conditions varchar(100), 
surgeries varchar(100), 
medicatation varchar(100)
);

create table Appointment( 
doctor_id int NOT NULL references Doctor(doctor_id), 
p_name varchar(20),
p_email varchar(20) references Patient(email),
date DATE NOT NULL, 
starttime time NOT NULL, 
endtime time NOT NULL, 
status varchar(20)NOT NULL
);

create table Diagnose(
doctor_id int NOT NULL, 
p_name varchar(20) NOT NULL, 
p_email varchar(20) NOT NULL,
diagnosis varchar(50) NOT NULL,
prescription varchar(50) NOT NULL
);





INSERT INTO Department (dept_id, dept_name) VALUES
(5001, 'Cardiology'),
(5002, 'Orthopedics'),
(5003, 'Pediatrics'),
(5004, 'Oncology'),
(5005, 'Gynaecology');
INSERT INTO Doctor (doctor_id, doctor_name, department_id, email, gender, password) VALUES
(1002, 'Dr. Smith', '5001', 'smith@gmail.com', 'm', 'password123'),
(1003, 'Dr. Johnson', '5002', 'johnson@gmail.com', 'f', 'pass456'),
(1004, 'Dr. William', '5002', 'william@gmail.com', 'm', 'pass455'),
(1005, 'Dr. Bree', '5004', 'bree@gmail.com', 'f', 'pass134'),
(1006, 'Dr. Sam', '5003', 'sam@gmail.com', 'm', 'pass111');

INSERT INTO Schedule (id, starttime, endtime, breaktime, day) VALUES
(1001, '08:00:00', '17:00:00', '12:00:00', 'Monday'),
(1002, '09:00:00', '18:00:00', '13:00:00', 'Tuesday'),
(1002, '09:00:00', '20:00:00', '15:00:00', 'Monday'),
(1003, '10:00:00', '18:00:00', '13:00:00', 'Wednesday'),
(1004, '08:00:00', '19:00:00', '13:00:00', 'Wedenesday'),
(1004, '11:00:00', '19:30:00', '15:00:00', 'Friday'),
(1005, '09:00:00', '18:00:00', '12:00:00', 'Tuesday'),
(1005, '12:30:00', '16:00:00', '14:00:00', 'Thursday');

INSERT INTO Staff (staff_id, staff_name, designation, availability) VALUES
(1, 'John Doe', 'Nurse', 'Yes'),
(2, 'Darwin', 'Receptionist', 'Yes'),
(3, 'Gill', 'Attendant', 'No'),
(4, 'Max', 'Receptionist', 'No'),
(5, 'Jane ', 'Receptionist', 'Yes');

INSERT INTO Patient (name, addr, gender, email, password) VALUES
('Alice Smith', '123 Main St, Bangalore', 'f', 'alice@gmail.com', 'pass123'),
('Bob Johnson', '456 Oak St, Pune', 'm', 'bob@gmail.com', 'pass456'),
('Smith C', '123 Church St Bangalore', 'f', 'smith@gmail.com', 'pass001'),
('Johnson L', '456 pearl St Chennai', 'm', 'john@gmail.com', 'pass432'),
('Alice W', '123 mid St, Mumbai', 'f', 'ali@gmail.com', 'pass103');
INSERT INTO Appointment VALUES
(1001,'Alice Smith', 'alice@gmail.com', '2022-07-10', '10:00:00', '10:30:00', 'Scheduled'),
(1001,'Alice Smith', 'alice@gmail.com', '2022-03-15', '14:00:00', '14:30:00', 'Completed'),
(1002,'Bob Johnson', 'bob@gmail.com', '2022-06-10', '11:00:00', '11:30:00', 'Scheduled'),
(1003,'Smith C', 'smith@gmail.com', '2022-09-15', '15:00:00', '15:30:00', 'Completed'),
(1003,'Bob Johnson', 'bob@gmail.com', '2022-05-11', '11:00:00', '12:30:00', 'Scheduled'),
(1003,'Smith C', 'smith@gmail.com', '2022-05-10', '16:00:00', '17:30:00', 'Scheduled'),
(1004,'Johnson L', 'john@gmail.com', '2022-06-10', '16:30:00', '17:30:00', 'Scheduled'),
(1005,'Alice W', 'ali@gmail.com','2022-05-10', '15:00:00', '16:30:00', 'Scheduled');

INSERT INTO Patientlist VALUES
(1001,'Alice Smith', 'alice@gmail.com','Dr. A','2022-03-15', 'High Blood Pressure','No', 'Prescription A'),
(1002,'Bob Johnson', 'bob@gmail.com', 'Dr. B','2022-05-07', 'Knee Injury', 'Knee Surgery', 'Prescription B'),
(1003,'Smith C', 'smith@gmail.com' ,'Dr. D','2022-05-07','Viral','No', 'Prescription A'),
(1003,'Bob Johnson', 'bob@gmail.com','Dr. A', '2022-08-08', 'Viral', 'No', 'Prescription B'),
(1004,'Johnson L', 'john@gmail.com','Dr. C','2022-06-07','Type 1 Diabetes','No', 'Prescription C'),
(1005,'Alice W','ali@gmail.com','Dr. C','2022-05-07', 'High Blood Pressure','No', 'Prescription A');