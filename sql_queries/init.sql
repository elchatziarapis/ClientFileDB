-- Drop tables if they exist
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS folders;

-- Create the folders table
-- unique_folder_name_per_parent: Ensures that within the same parent folder, folder names are unique.
-- no_self_reference: Prevents a folder from being its own parent.
CREATE TABLE folders (
    folder_id SERIAL PRIMARY KEY,
    folder_name VARCHAR(255) NOT NULL,
    folder_parent_id INTEGER,
    FOREIGN KEY (folder_parent_id) REFERENCES folders (folder_id),
    CONSTRAINT unique_folder_name_per_parent UNIQUE (folder_parent_id, folder_name),
    CONSTRAINT no_self_reference CHECK (folder_id <> folder_parent_id)
);

-- Ensure only one root folder
-- unique_root_folder: Ensures there can only be one root folder (where folder_parent_id is null)
CREATE UNIQUE INDEX unique_root_folder ON folders ((folder_parent_id IS NULL)) WHERE folder_parent_id IS NULL;

-- Create the files table with ON DELETE CASCADE
-- ON DELETE CASCADE: Ensures that when a folder is deleted, all files within that folder are also deleted.
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    file_created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    folder_id INTEGER NOT NULL,
    file_s3_key VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT unique_file_name_per_folder UNIQUE (folder_id, file_name),
    FOREIGN KEY (folder_id) REFERENCES folders (folder_id) ON DELETE CASCADE
);

-- Create indexes for the folders table
-- idx_folder_parent_id: Index on folder_parent_id to improve query performance when searching by parent folder
CREATE INDEX idx_folder_parent_id ON folders (folder_parent_id);

-- Create indexes for the files table
-- idx_file_folder_id: Index on folder_id to improve query performance when searching by folder
-- idx_file_s3_key: Index on file_s3_key to improve query performance when searching by S3 key
CREATE INDEX idx_file_folder_id ON files (folder_id);
CREATE INDEX idx_file_s3_key ON files (file_s3_key);
