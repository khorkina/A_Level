import os
import streamlit as st
import tempfile
from utils.zip_handler import extract_zip_structure, get_file_structure
from utils.pdf_handler import display_pdf

# Set page configuration
st.set_page_config(
    page_title="A Level Study Resources",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'zip_path' not in st.session_state:
    st.session_state['zip_path'] = None
if 'extracted_dir' not in st.session_state:
    st.session_state['extracted_dir'] = None
if 'file_structure' not in st.session_state:
    st.session_state['file_structure'] = None
if 'current_file' not in st.session_state:
    st.session_state['current_file'] = None
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []

# Main title
st.title("A Level Study Resources")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    
    # Upload zip file
    uploaded_zip = st.file_uploader("Upload A Level content zip file", type="zip")
    
    if uploaded_zip is not None and (st.session_state.zip_path is None or uploaded_zip.name != os.path.basename(st.session_state.zip_path)):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(uploaded_zip.getbuffer())
            st.session_state.zip_path = tmp_file.name
        
        # Extract the zip file
        try:
            st.session_state.extracted_dir = extract_zip_structure(st.session_state.zip_path)
            st.session_state.file_structure = get_file_structure(st.session_state.extracted_dir)
            st.success("Zip file successfully extracted!")
        except Exception as e:
            st.error(f"Error extracting zip file: {e}")
            st.session_state.zip_path = None
    
    # Search functionality
    st.subheader("Search")
    search_query = st.text_input("Search for topics or files")
    
    if search_query and st.session_state.file_structure:
        # Search for files/folders that match the query
        search_results = []
        for path, is_dir, parent in st.session_state.file_structure:
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
    if st.session_state.file_structure:
        st.subheader("Subjects and Topics")
        
        # Get all top-level directories (subjects)
        subjects = [
            (path, name) 
            for path, is_dir, parent in st.session_state.file_structure 
            if is_dir and parent == st.session_state.extracted_dir
        ]
        
        # Group files by subject
        for subject_path, _ in subjects:
            subject_name = os.path.basename(subject_path)
            with st.expander(f"📚 {subject_name}"):
                # Get topics within this subject
                topics = [
                    (path, is_dir)
                    for path, is_dir, parent in st.session_state.file_structure
                    if parent == subject_path
                ]
                
                for topic_path, is_topic_dir in topics:
                    topic_name = os.path.basename(topic_path)
                    
                    if is_topic_dir:
                        # This is a topic folder
                        st.write(f"📂 {topic_name}")
                        
                        # Display files within this topic
                        topic_files = [
                            path
                            for path, is_dir, parent in st.session_state.file_structure
                            if not is_dir and parent == topic_path
                        ]
                        
                        for file_path in topic_files:
                            file_name = os.path.basename(file_path)
                            if st.button(f"📄 {file_name}", key=file_path):
                                st.session_state.current_file = file_path
                                st.rerun()
                    else:
                        # This is a file directly under the subject
                        if st.button(f"📄 {topic_name}", key=topic_path):
                            st.session_state.current_file = topic_path
                            st.rerun()

# Main content area
if st.session_state.zip_path is None:
    st.info("Please upload an A Level content zip file to get started.")
    
    # Additional instructions
    st.markdown("""
    ## Getting Started
    
    1. Use the file uploader in the sidebar to upload your A Level content zip file
    2. Navigate through subjects and topics using the sidebar
    3. Click on any file to view its contents
    4. Use the search box to find specific topics or files
    
    This application allows you to organize and access your A Level study materials in a structured way.
    """)
else:
    if st.session_state.current_file:
        file_name = os.path.basename(st.session_state.current_file)
        st.subheader(f"Viewing: {file_name}")
        
        if file_name.lower().endswith('.pdf'):
            display_pdf(st.session_state.current_file)
        elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            st.image(st.session_state.current_file, caption=file_name)
        elif file_name.lower().endswith(('.txt', '.csv')):
            with open(st.session_state.current_file, 'r') as f:
                content = f.read()
            st.text_area("File content", content, height=300)
        else:
            st.warning(f"Cannot display this file type. File: {file_name}")
    else:
        st.info("Select a file from the sidebar to view its contents.")
        
        # Display welcome message with instructions
        st.markdown("""
        ## Welcome to A Level Study Resources!
        
        This application helps you organize and access your A Level study materials.
        
        **Instructions:**
        1. Use the sidebar to navigate through subjects and topics
        2. Click on any file to view its contents
        3. Use the search box to find specific topics or files
        
        Happy studying!
        """)
