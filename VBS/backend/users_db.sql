
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    description TEXT,
    projects TEXT,  -- List of project IDs saved in the 'projects' database
    birthdate DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
 );


--INSERT INTO users (name, surname, username, email, password, description, projects, birthdate) VALUES
--('John', 'Doe', 'johndoe', 'jon.hey@gmail.com', 'password123', 'A software developer from NY.', '23,31', '1990-05-15'),
--('Jane', 'Smith', 'janesmith', 'jane.smith@gmail.com', 'password456', 'A marketing specialist from LA.', '2,21', '1988-12-20'),
--('Thomas', 'Battaglia', 'BatThommy', 'batthommy@gmail.com', 'pppassword', 'The BOSS', '24,25', '2013-01-20');

-- THE TEST USERS AREN'T VALID ANYMORE BECAUSE THE PASSWORDS ARE HASHED AND SALTED IN THE DB



