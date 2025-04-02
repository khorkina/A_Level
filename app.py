"""
A Level Study Resources - Streamlit Application
"""

import os
import streamlit as st
from utils.pdf_handler import display_pdf

# Define constants
STATIC_CONTENT_PATH = "static_content"
EXAM_MATERIALS_PATH = os.path.join(STATIC_CONTENT_PATH, "ALEVEL", "EXAM_MATERIALS")

# Configure the page
st.set_page_config(
    page_title="A Level Study Resources",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the appearance
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    .st-emotion-cache-16idsys {
        font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Function to get files in a directory
def get_files_in_directory(directory):
    """
    Get a list of files in a directory.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        list: List of file paths
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# Function to get the file structure
def get_file_structure(directory):
    """
    Get a dictionary with the file structure.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        dict: Dictionary with the file structure
    """
    structure = {}
    
    # Check if the directory exists
    if not os.path.exists(directory):
        st.error(f"Directory not found: {directory}")
        st.error("Please make sure you've extracted the ALEVEL.zip file correctly.")
        st.error("Run the setup script: `python setup.py`")
        return structure
    
    # Get all the subjects (top-level directories)
    subjects = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    for subject in subjects:
        subject_path = os.path.join(directory, subject)
        structure[subject] = {}
        
        # Get all the topics (second-level directories)
        topics = [d for d in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, d))]
        
        for topic in topics:
            topic_path = os.path.join(subject_path, topic)
            structure[subject][topic] = []
            
            # Get all files in the topic directory
            for root, _, files in os.walk(topic_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, topic_path)
                    structure[subject][topic].append({
                        'name': relative_path,
                        'path': file_path
                    })
    
    return structure

# Define the title and introduction
st.title("A Level Study Resources 📚")
st.markdown("""
Welcome to the A Level Study Resources application! This tool is designed to help
you navigate and access A Level study materials for various subjects.

Browse the subjects and topics in the sidebar, and click on any file to view its contents.
""")

# Get the file structure
file_structure = get_file_structure(EXAM_MATERIALS_PATH)

# Create sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    
    # Create a search box
    search_query = st.text_input("Search for topics or files:", "")
    
    # Display the file structure
    selected_subject = st.selectbox("Select Subject:", list(file_structure.keys()))
    
    if selected_subject:
        selected_topic = st.selectbox("Select Topic:", list(file_structure[selected_subject].keys()))
        
        if selected_topic:
            # Filter files based on search query if provided
            files = file_structure[selected_subject][selected_topic]
            if search_query:
                files = [f for f in files if search_query.lower() in f['name'].lower()]
            
            # Display the files
            st.write("Files:")
            for file in files:
                if st.button(file['name'], key=file['path']):
                    st.session_state.selected_file = file['path']

# Display the selected file
if 'selected_file' in st.session_state:
    file_path = st.session_state.selected_file
    file_name = os.path.basename(file_path)
    
    st.header(f"Viewing: {file_name}")
    
    # Display the file based on its extension
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext in ['.pdf']:
        display_pdf(file_path)
    elif file_ext in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            st.text(f.read())
    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
        st.image(file_path)
    else:
        st.warning(f"Cannot display file of type: {file_ext}")
        st.write("You can download the file instead.")
        
    # Add a download button
    with open(file_path, "rb") as file:
        st.download_button(
            label="Download File",
            data=file,
            file_name=file_name,
            mime="application/octet-stream"
        )