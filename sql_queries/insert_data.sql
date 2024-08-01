-- Insert root folder
INSERT INTO folders (folder_name, folder_parent_id) VALUES
('/', NULL);

-- Insert directories under root
INSERT INTO folders (folder_name, folder_parent_id) VALUES
('bin', 1),
('boot', 1),
('dev', 1),
('etc', 1),
('home', 1),
('opt', 1),
('root', 1),
('sbin', 1),
('tmp', 1),
('usr', 1),
('var', 1);

INSERT INTO folders (folder_name, folder_parent_id) VALUES
('cron.d', 4),
('cron.daily', 4),
('cron.hourly', 4),
('cron.monthly', 4),
('cron.weekly', 4);

-- Insert directories under /home
INSERT INTO folders (folder_name, folder_parent_id) VALUES
('user1', 5),        
('user2', 5);

-- Insert directories under /opt
INSERT INTO folders (folder_name, folder_parent_id) VALUES
('s1', 6),    
('s2', 6);

-- Insert directories under /sbin
INSERT INTO folders (folder_name, folder_parent_id) VALUES
('ntw', 8);

INSERT INTO files (file_name, file_size, folder_id, file_s3_key) VALUES
('ls', 1111, 2, 's3_temp_ls'),
('cp', 5535, 2, 's3_temp_cp'),
('mv', 2343, 2, 's3_temp_mv');