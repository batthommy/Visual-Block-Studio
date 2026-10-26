INSERT INTO top3 (category, position, title, description, image)
VALUES
(1, 1, 'Project Alpha', 'A project about alpha testing.', 'project.png'),
(1, 2, 'Project Beta', 'A project about beta testing.', 'project.png'),
(1, 3, 'Project Gamma', 'A project about gamma rays.', 'project.png'),

(2, 1, 'Project delta', 'A project about delta testing.', 'project.png'),
(2, 2, 'Project Alpha', 'A project about alpha testing.', 'project.png'),
(2, 3, 'Project Beta', 'A project about beta testing.', 'project.png'),

(3, 1, 'Project Gamma', 'A project about gamma rays.', 'project.png'),
(3, 2, 'Project delta', 'A project about delta testing.', 'project.png'),
(3, 3, 'Project Alpha', 'A project about alpha testing.', 'project.png')
ON CONFLICT(category, position) DO UPDATE SET
    title = excluded.title,
    description = excluded.description,
    image = excluded.image;