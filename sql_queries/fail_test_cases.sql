-- Test queries that must produce errors

-- 1. Unique Folder Name Constraint Violation
-- Attempt to insert a folder with a name that already exists under the same parent folder.
INSERT INTO folders (folder_name, folder_parent_id) VALUES ('bin', 1);

-- 2. Self-Referencing Parent ID Violation
-- Attempt to update a folder to have a parent ID that is the same as its own folder ID.
UPDATE folders
SET folder_parent_id = folder_id
WHERE folder_id = 2;

-- 3. Multiple Root Folders Violation
-- Attempt to insert another root folder with a NULL parent_id.
INSERT INTO folders (folder_name, folder_parent_id) VALUES ('roooooot', NULL); -- Should fail if another root folder is inserted.

-- 4. Invalid Folder ID in Update
-- Attempt to update a folder to have a parent ID that does not exist.
UPDATE folders
SET folder_parent_id = 99999 
WHERE folder_id = 3;
SELECT * FROM folders

-- 5. Duplicate Folder Name with Existing Folder
-- Attempt to insert a folder with a name that already exists under the same parent folder.
INSERT INTO folders (folder_name, folder_parent_id) VALUES ('user1', 5);

-- 6. Moving Folder to Invalid Parent
-- Attempt to update a folder's parent ID to an invalid value.
UPDATE folders
SET folder_parent_id = 99999
WHERE folder_id = 7;

-- 7. Updating Folder Name to an Existing Name Under the Same Parent
-- Attempt to update a folder's name to one that already exists under the same parent.
UPDATE folders
SET folder_name = 'var'
WHERE folder_id = 8;