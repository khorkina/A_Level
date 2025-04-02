import os
import streamlit as st
from utils.pdf_handler import display_pdf

# Set page configuration
st.set_page_config(
    page_title="A Level Study Resources",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path to the static content extracted from the zip file
STATIC_CONTENT_PATH = "static_content/ALEVEL/EXAM_MATERIALS"

# Initialize session state for current file
if 'current_file' not in st.session_state:
    st.session_state['current_file'] = None
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []

# Function to get all files in a directory recursively
def get_files_in_directory(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

# Function to get file structure
def get_file_structure(directory):
    structure = []
    for root, dirs, files in os.walk(directory):
        # Add directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            structure.append((dir_path, True, root))
        
        # Add files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            structure.append((file_path, False, root))
    
    return structure

# Get all files and file structure
all_files = get_files_in_directory(STATIC_CONTENT_PATH)
file_structure = get_file_structure(STATIC_CONTENT_PATH)

# Main title
st.title("A Level Study Resources")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    
    # Search functionality
    st.subheader("Search")
    search_query = st.text_input("Search for topics or files")
    
    if search_query:
        # Search for files/folders that match the query
        search_results = []
        for path, is_dir, parent in file_structure:
            if search_query.lower() in os.path.basename(path).lower():
                search_results.append((path, is_dir, parent))
        
        st.session_state.search_results = search_results
        
        if search_results:
            st.subheader("Search Results")
            for idx, (path, is_dir, _) in enumerate(search_results):
                file_name = os.path.basename(path)
                if is_dir:
                    st.write(f"📁 {file_name}")
                else:
                    if st.button(f"📄 {file_name}", key=f"search_{idx}"):
                        st.session_state.current_file = path
                        st.rerun()
        else:
            st.info("No matching results found")
    
    # Display file structure for navigation
    st.subheader("Subjects and Topics")
    
    # Get all top-level directories (subjects)
    subject_dirs = [d for d in os.listdir(STATIC_CONTENT_PATH) if os.path.isdir(os.path.join(STATIC_CONTENT_PATH, d))]
    
    # Group files by subject
    for subject_dir in subject_dirs:
        subject_path = os.path.join(STATIC_CONTENT_PATH, subject_dir)
        subject_name = subject_dir.replace("_Materials", "")
        
        with st.expander(f"📚 {subject_name}"):
            # Get topics within this subject
            topic_paths = [
                os.path.join(subject_path, d) 
                for d in os.listdir(subject_path) 
                if os.path.isdir(os.path.join(subject_path, d))
            ]
            
            # Get files directly in subject folder
            subject_files = [
                os.path.join(subject_path, f)
                for f in os.listdir(subject_path)
                if os.path.isfile(os.path.join(subject_path, f))
            ]
            
            # Display files directly under the subject
            for file_path in subject_files:
                file_name = os.path.basename(file_path)
                if st.button(f"📄 {file_name}", key=file_path):
                    st.session_state.current_file = file_path
                    st.rerun()
            
            # Display topics and their files
            for topic_path in topic_paths:
                topic_name = os.path.basename(topic_path)
                st.write(f"📂 {topic_name}")
                
                # Get files within this topic
                if os.path.isdir(topic_path):
                    try:
                        topic_files = [
                            os.path.join(topic_path, f)
                            for f in os.listdir(topic_path)
                            if os.path.isfile(os.path.join(topic_path, f))
                        ]
                        
                        for file_path in topic_files:
                            file_name = os.path.basename(file_path)
                            if st.button(f"📄 {file_name}", key=file_path):
                                st.session_state.current_file = file_path
                                st.rerun()
                    except Exception as e:
                        st.error(f"Error accessing {topic_path}: {e}")

# Main content area
if st.session_state.current_file:
    file_name = os.path.basename(st.session_state.current_file)
    st.subheader(f"Viewing: {file_name}")
    
    if file_name.lower().endswith('.pdf'):
        display_pdf(st.session_state.current_file)
    elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        st.image(st.session_state.current_file, caption=file_name)
    elif file_name.lower().endswith(('.txt', '.csv')):
        try:
            with open(st.session_state.current_file, 'r') as f:
                content = f.read()
            st.text_area("File content", content, height=300)
        except UnicodeDecodeError:
            st.error("Unable to display this file type due to encoding issues.")
    else:
        st.warning(f"Cannot display this file type. File: {file_name}")
else:
    st.info("Select a file from the sidebar to view its contents.")
    
    # Display welcome message with instructions
    st.markdown("""
    ## Welcome to A Level Study Resources!
    
    This application helps you access A Level study materials for various subjects.
    
    **Instructions:**
    1. Use the sidebar to navigate through subjects and topics
    2. Click on any file to view its contents
    3. Use the search box to find specific topics or files
    
    ### Available Subjects:
    - Business
    - English
    - Psychology
    - Sociology
    
    Happy studying!
    """)
