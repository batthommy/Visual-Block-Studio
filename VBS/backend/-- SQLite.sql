-- SQLite

-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     surname TEXT,
--     username TEXT NOT NULL UNIQUE,
--     email TEXT NOT NULL,
--     password TEXT NOT NULL,
    -- description TEXT,
--     projects TEXT,  -- List of project IDs saved in the 'projects' database
--     birthdate DATE,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- );


-- INSERT INTO users (name, surname, username, email, password, description, projects, birthdate) VALUES
-- ('John', 'Doe', 'johndoe', 'jon.hey@gmail.com', 'password123', 'A software developer from NY.', '23,31', '1990-05-15'),
-- ('Jane', 'Smith', 'janesmith', 'jane.smith@gmail.com', 'password456', 'A marketing specialist from LA.', '2,21', '1988-12-20'),
-- ('Thomas', 'Battaglia', 'BatThommy', 'batthommy@gmail.com', 'pppassword', 'The BOSS', '24,25', '2013-01-20');





-- CREATE TABLE projects (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     description TEXT,
--     owner_id INTEGER NOT NULL,  -- Reference to the user who owns the project
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     code TEXT NOT NULL,
--     FOREIGN KEY (owner_id) REFERENCES users(id)
-- );


-- INSERT INTO projects (name, description, owner_id, code) VALUES
-- ('Project Alpha', 'A project about alpha testing.', 1, 'ALPHA123'),
-- ('Project Beta', 'A project about beta testing.', 3, 'BETA456'),
-- ('Project Gamma', 'A project about gamma rays.', 2, 'GAMMA789'),
-- ('Project delta', 'A project about delta testing.', 3, 'DELTA012');