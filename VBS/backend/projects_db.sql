 
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL,  -- Reference to the user who owns the project
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    code TEXT NOT NULL,
    flags TEXT NOT NULL,  -- List of flags saved in the 'flags' database
    FOREIGN KEY (owner_id) REFERENCES users(id)
 );


 INSERT INTO projects (name, description, owner_id, code, flags) VALUES
 ('Project Alpha', 'A project about alpha testing.', 1, 'ALPHA123', 'flag1,flag2'),
 ('Project Beta', 'A project about beta testing.', 3, 'BETA456', 'flag3,flag4'),
 ('Project Gamma', 'A project about gamma rays.', 2, 'GAMMA789', 'flag5,flag6'),
 ('Project delta', 'A project about delta testing.', 3, 'DELTA012', 'flag7,flag8');