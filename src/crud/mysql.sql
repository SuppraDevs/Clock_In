CREATE TABLE students (
    rfID varchar(100) NOT NULL,
    nameStudent varchar (255),
    presenceStudent int,
    absenceStudent int,
    lateStudent int,
    isPresent tinyint(1) default 0,
    PRIMARY KEY (rfID)
);


CREATE TABLE entrance_table (
    idEntrance int AUTO_INCREMENT,
    timeEntrance TIMESTAMP,
    rfID varchar (100),
    PRIMARY KEY (idEntrance),
    FOREIGN KEY (rfID) REFERENCES students(rfID)
);


CREATE TABLE general_attendance (
    rfID varchar(100) NOT NULL,
    nameStudent varchar (255),
    presenceStudent int,
    absenceStudent int,
    lateStudent int,
    FOREIGN KEY (rfID) REFERENCES students(rfID)
);


CREATE TABLE exit_table (
    idExit int AUTO_INCREMENT,
    timeExit TIMESTAMP,
    rfID varchar (100),
    PRIMARY KEY (idExit),
    FOREIGN KEY (rfID) REFERENCES students(rfID)
);


INSERT INTO entrance_table (timeEntrace, rfID)
VALUES ("{current_time}, {rfID}");

INSERT INTO exit_table (timeExit, rfID)
VALUES ("{current_time}, {rfID}");

INSERT INTO general_attendance (rfID, nameStudent, presenceStudent, absenceStudent, lateStudent) VALUES ("0001", "Celso Ricardo", 0, 0, 0);




UPDATE students
SET presenceStudent = 0, lateStudent = 0, absenceStudent = 0, isPresent = 0
WHERE rfID = '383529815217';

UPDATE students
SET presenceStudent = 0, lateStudent = 0, absenceStudent = 0, isPresent = 0
WHERE rfID = '667350401237';

UPDATE general_attendance
SET presenceStudent = 0, lateStudent = 0, absenceStudent = 0
WHERE rfID = '667350401237';

UPDATE general_attendance
SET presenceStudent = 0, lateStudent = 0, absenceStudent = 0
WHERE rfID = '383529815217';




SELECT presenceStudent FROM students WHERE rfID = '123';


UPDATE general_attendance 
SET presenceStudent = {new_presence}, absenceStudent = {new_abscence}, lateStudent = {lateness}