"""
Zip file handling utilities for the A Level Study Resources application.
"""

import os
import zipfile
import shutil


def extract_zip_structure(zip_path, extract_to=None):
    """
    Extract the contents of a zip file to a temporary directory.
    
    Args:
        zip_path (str): Path to the zip file
        extract_to (str, optional): Path to extract the zip file to. 
                                   If None, a temporary directory will be created.
        
    Returns:
        str: Path to the directory where the zip file was extracted
    """
    if extract_to is None:
        extract_to = "temp_extract"
        
    # Create the extraction directory if it doesn't exist
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
        
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        
    return extract_to


def get_file_structure(directory):
    """
    Get the structure of files and directories in the given directory.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        list: List of tuples (path, is_directory, parent_directory)
    """
    file_structure = []
    
    for root, dirs, files in os.walk(directory):
        # Add directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            parent_dir = os.path.basename(root)
            file_structure.append((dir_path, True, parent_dir))
            
        # Add files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            parent_dir = os.path.basename(root)
            file_structure.append((file_path, False, parent_dir))
            
    return file_structure


def move_extracted_content(source_dir, dest_dir):
    """
    Move the extracted content to a permanent location.
    
    Args:
        source_dir (str): Path to the source directory
        dest_dir (str): Path to the destination directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        # Copy the contents
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
                
        return True
    except Exception as e:
        print(f"Error moving extracted content: {e}")
        return False