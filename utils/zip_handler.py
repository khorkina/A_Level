import os
import zipfile
import tempfile
import shutil

def extract_zip_structure(zip_path):
    """
    Extract the contents of a zip file to a temporary directory.
    
    Args:
        zip_path (str): Path to the zip file
        
    Returns:
        str: Path to the directory where the zip file was extracted
    """
    # Create a temporary directory to extract the zip file
    extract_dir = tempfile.mkdtemp()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except Exception as e:
        # Clean up the temporary directory if extraction fails
        shutil.rmtree(extract_dir, ignore_errors=True)
        raise Exception(f"Failed to extract zip file: {e}")
    
    return extract_dir

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
            file_structure.append((dir_path, True, root))
        
        # Add files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_structure.append((file_path, False, root))
    
    return file_structure
