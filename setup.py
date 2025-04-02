#!/usr/bin/env python3
"""
Setup script to prepare the A Level Study Resources application.
This script extracts the zip file and ensures the directory structure is correct.
"""

import os
import zipfile
import shutil
import sys

def main():
    """Main setup function to extract the zip file."""
    print("Setting up A Level Study Resources application...")
    
    # Check if the zip file exists
    zip_path = os.path.join("attached_assets", "ALEVEL.zip")
    if not os.path.exists(zip_path):
        print(f"Error: Zip file not found at {zip_path}")
        print("Please place the ALEVEL.zip file in the 'attached_assets' directory.")
        return 1
    
    # Create the static_content directory if it doesn't exist
    static_dir = "static_content"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Extract the zip file
    try:
        print(f"Extracting {zip_path} to {static_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(static_dir)
        print("Extraction complete!")
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return 1
    
    # Check if the extraction was successful
    extracted_path = os.path.join(static_dir, "ALEVEL", "EXAM_MATERIALS")
    if not os.path.exists(extracted_path):
        print(f"Error: Expected directory structure not found at {extracted_path}")
        return 1
    
    print("\nSetup completed successfully!")
    print("\nTo run the application, use the following command:")
    print("    streamlit run app.py")
    print("\nThe application will be available at http://localhost:8501")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())