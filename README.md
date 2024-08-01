# File System Database

## Overview
This project is a highly optimized file system database with a client application to manage files and folders. It includes functionalities to create, move, and delete files and folders, and to calculate the total size of a folder's contents. All the meta data will be stored in the database but the original files are stored in Amazon S3, ensuring scalable and reliable storage.

## Functional Requirements

- The system must allow users to create, move, and delete both folders and files, handling nested structures correctly.
- It should provide functionality to list all contents within a specified folder and retrieve detailed information about individual files, such as name, size, and creation date.
- The system must support calculating the total size of all files within a given folder and its subfolders.
- Files must be stored in Amazon S3 for scalable and reliable storage.
- When deleting folders, all nested files and subfolders must also be deleted.
- Only one root folder must exist in the system at any time.
- No two files or folders can have the same name and the same parent.


## Non-Functional Requirements

- The system must perform efficiently with large datasets, maintaining quick response times for all operations.
- It should be scalable to handle increasing numbers of files and folders without performance issues.
- The client application needs to offer an intuitive and user-friendly interface, with robust error handling and clear instructions.
- Data integrity must be preserved across all operations, ensuring accurate size calculations and consistent state.

## Usage
### Folder Operations
- Create a folder
- Delete a folder
- Move a folder
- List folder contents

### File Operations
- Create a file
- Delete a file
- Move a file
- Get file details

### Size Calculation
- Get total size of files in a folder and its subfolders

### Services
- **File**
  - Create file records in the database.
  - Upload files to S3.
  - Delete files from the database and S3.
  - Fetch file details from the database.
  - Move file

- **Folder**
  - Create folder records in the database.
  - Move folders within the hierarchy.
  - Calculate folder size including all nested files.
  - List files and subfolders recursively.
  - Delete folders and all nested contents from the database and S3.