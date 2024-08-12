import os
import json
import base64

def get_profile_path(profile_id, profile_name):
    """
    Create the full path to the given profile for the current user.

    Parameters:
    - profile_id (str): The ID of the profile.
    - profile_name (str): The name of the profile.

    Returns:
    - str: The full path to the profile file for the current user.
    """
    user_home_directory = os.path.expanduser("~")
    return os.path.join(user_home_directory, profile_id + profile_name)

def load_profile_from_file(file_path):
    """
    Load and decode a profile from a file.

    Parameters:
    - file_path (str): The path to the profile file.

    Returns:
    - dict: The profile data decoded from the file.
    """
    with open(file_path, 'rb') as file:
        encoded_data = file.read()
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    return json.loads(decoded_data)

def load_from_json(file_path):
    """
    Load and decode data from a JSON file, returning it as a dictionary.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: The data decoded from the JSON file. Returns None if the file does not exist.
    """
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            encoded_data = file.read()
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)
    return None

def save_to_json(file_path, data):
    """
    Encode and save data to a JSON file.

    Parameters:
    - file_path (str): The path where the JSON file will be saved.
    - data (dict): The data to be encoded and saved.

    Returns:
    - None
    """
    with open(file_path, 'wb') as file:
        json_data = json.dumps(data)
        encoded_data = base64.b64encode(json_data.encode('utf-8'))
        file.write(encoded_data)