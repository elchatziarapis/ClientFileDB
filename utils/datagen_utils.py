import pandas as pd
import numpy as np

def generate_data(num_folders: int, num_files: int, start_date: str = '2023-01-01', date_range_days: int = 365) -> None:
    """
    Generate random data for folders and files and save them to CSV files.

    Args:
        num_folders (int): Number of folders to generate.
        num_files (int): Number of files to generate.
        start_date (str, optional): Start date for file creation dates. Defaults to '2023-01-01'.
        date_range_days (int, optional): Number of days to generate dates over. Defaults to 365.

    Returns:
        None: This function saves generated data to 'folders.csv' and 'files.csv'.
    """
    
    folder_ids = np.arange(1, num_folders + 1)
    folder_names = [f'Folder{i}' for i in range(1, num_folders + 1)]
    folder_parent_ids = [None] + [np.random.choice(folder_ids[:i]) for i in range(1, num_folders)]

    folders_data = {
        'folder_id': folder_ids,
        'folder_name': folder_names,
        'folder_parent_id': folder_parent_ids
    }
    folders_df = pd.DataFrame(folders_data)
    folders_df['folder_parent_id'] = folders_df['folder_parent_id'].astype(pd.Int64Dtype())

    while folders_df.duplicated(subset=['folder_parent_id', 'folder_name']).any():
        for idx, row in folders_df.iterrows():
            if folders_df.duplicated(subset=['folder_parent_id', 'folder_name']).iloc[idx]:
                folders_df.at[idx, 'folder_name'] = row['folder_name'] + '_new'

    date_range = pd.date_range(start=start_date, periods=date_range_days)
    creation_dates = np.random.choice(date_range, size=num_files)
    
    files_data = {
        'file_id': np.arange(1, num_files + 1),
        'file_name': [f'File{i}' for i in range(1, num_files + 1)],
        'file_size': np.random.randint(100, 10000, size=num_files),
        'file_created_date': creation_dates,
        'folder_id': np.random.choice(folders_data['folder_id'], size=num_files),
        'file_s3_key': [f's3_key_{i}' for i in range(1, num_files + 1)]
    }
    files_df = pd.DataFrame(files_data)
    folders_df.to_csv('folders.csv', index=False)
    files_df.to_csv('files.csv', index=False)

    print(f"CSV files created successfully with {num_folders} folders and {num_files} files!")

num_folders = 100
num_files = 5000000

generate_data(num_folders, num_files)
