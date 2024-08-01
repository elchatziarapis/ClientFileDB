-- All folder names with the same parent
SELECT folder_parent_id, folder_name
FROM folders
WHERE folder_parent_id = 1;

-- Total size of files in every folder
SELECT folder_id, COALESCE(SUM(file_size), 0) AS total_size
FROM files
GROUP BY folder_id;