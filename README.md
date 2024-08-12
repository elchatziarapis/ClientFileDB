# File System Database

## Overview
This project is a highly optimized file system database with a client application to manage files and folders. It includes functionalities to create, move, and delete files and folders, and to calculate the total size of a folder's contents. All the meta data will be stored in the database but the original files are stored in Amazon S3, ensuring scalable and reliable storage.

## Objectives

1. **Database Design**: Create a database schema that efficiently stores and manages a large number of files and folders.
2. **Client Application**: Develop a client application that interacts with the database, providing functionalities for file and folder operations.

### Database Design

1. **Schema Design**:
   - **Folders**: Each folder has a name and may have a parent folder.
   - **Files**: Each file has a name, size, creation date, and a reference to its containing folder.

2. **Indexing**: Implement indexes to ensure efficient querying, especially for operations involving large datasets.

### Client Application

1. **Folder Operations**:
   - Create a new folder.
   - Delete an existing folder.
   - Move a folder to a different location.
   - List all files and subfolders within a folder.

2. **File Operations**:
   - Create a new file within a specified folder.
   - Delete an existing file.
   - Move a file to a different folder.
   - Retrieve file details (name, size, creation date).

3. **Size Calculation**:
   - Retrieve the total size of all files within a given folder and its subfolders (similar to the `du` command in Linux).

## Evaluation Criteria

1. **Correctness**: The database schema and application functionality should meet the specified requirements.
2. **Efficiency**: The solution should handle large datasets efficiently.
3. **Code Quality**: The code should be well-organized, commented, and adhere to best practices.
4. **Documentation**: Clear and concise documentation for setting up and using the system.
5. **Innovation**: Any additional features or improvements beyond the specified requirements will be considered favorably.


## Tools and Technologies

- **Database**: PostgreSQL
- **Programming Language**: Python 3
- **Version Control**: Git
- **File Storage**: Amazon S3

## Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/elchatziarapis/ClientFileDB.git
   cd ClientFileDB
   ```

2. **Set Up the Database**
    - If you haven't already, download and install PostgreSQL from the official [PostgreSQL website](https://www.postgresql.org/download/).

    -  Add PostgreSQL to the System PATH
        1. Open the Start Menu, search for "Environment Variables," and select "Edit the system environment variables."
        2. In the System Properties window, click on the "Environment Variables" button.
        3. In the Environment Variables window, find the "Path" variable in the "System variables" section and click "Edit."
        4. Click "New" and add the path to the PostgreSQL `bin` directory. This is usually something like `C:\Program Files\PostgreSQL\<version>\bin`.
        5. Click "OK" to close all windows.

    - Create the database and tables using the provided SQL script:
    ```
    psql -U yourname -v tablename='yourtable' -f sql_queries/init.sql
    ```
    - Also fill the tables with some test examples
    ```
    psql -U yourname -v tablename='yourtable' -f sql_queries/insert_data.sql
    ```

3. **Install Dependencies**
    - Create a virtual environment and install required packages:
    ```
    python -m venv venv 
    source venv/bin/activate  
    # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
4. **Configure the Application**
    - Fill necessary details, database credentials and also your AWS credentials and bucket name:
    ``` config/config.ini ```

## Usage

Run the main application:

```sh
python main.py --mode {cli,gui}
```

## Features


### Folder Operations
- **1. Create folder**: Create new folder records in the database.
- **2. Delete folder**: Delete folders and all nested contents from the database and S3.
- **3. Move folder**: Move folders within the hierarchy.
- **4. List files and subfolders**: List all files and subfolders within a folder recursively.
- **9. Calculate folder size**: Calculate the total size of a folder including all nested files.


### File Operations
- **5. Create file**: Create a new file record in the database and upload the file to S3.
- **6. Delete file**: Delete file records from the database and remove files from S3.
- **7. Move file**: Move files to a different folder within the hierarchy.
- **8. Get file details**: Retrieve detailed information about a file from the database.


## System Design Details

### Functional Requirements

- The system must allow users to create, move, and delete both folders and files, handling nested structures correctly.
- It should provide functionality to list all contents within a specified folder and retrieve detailed information about individual files, such as name, size, and creation date.
- The system must support calculating the total size of all files within a given folder and its subfolders.
- Files must be stored in Amazon S3 for scalable and reliable storage.
- When deleting folders, all nested files and subfolders must also be deleted.
- Only one root folder must exist in the system at any time.
- No two files or folders can have the same name and the same parent.


### Non-Functional Requirements

- The system must perform efficiently with large datasets, maintaining quick response times for all operations.
- It should be scalable to handle increasing numbers of files and folders without performance issues.
- The client application needs to offer an intuitive and user-friendly interface, with robust error handling and clear instructions.
- Data integrity must be preserved across all operations, ensuring accurate size calculations and consistent state.

### Alternative Ideas and future implementations

In case we turn this into a web application, there are multiple factors and ideas that can be used to create this magnificent project. I present my idea on how could this be done.

![System Design](https://github.com/user-attachments/assets/8f5ab778-b913-41d4-892b-80d3ee479a0b)



# Documentation

For additional documentation on the whole project we could use sphinx tool.

## Code Quality

- The code follows best practices and is well-organized and commented.
- Exception handling and logging are implemented to ensure robustness and traceability.

## Innovation

The project includes an efficient recursive function to fetch all subfolders and files, ensuring that the system can handle large datasets efficiently.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Thank you for using the File System Database Design and Client Application. If you have any questions or need further assistance, please contact [l.chatziarapis@gmail.com](mailto:l.chatziarapis@gmail.com).
