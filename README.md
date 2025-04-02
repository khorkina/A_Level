# A Level Study Resources App

A Streamlit-based web application for organizing and displaying A Level educational content, with PDF viewing capabilities.

## Description

This application provides an organized way to access A Level study materials across different subjects including:
- Business
- English
- Psychology
- Sociology

The app automatically extracts content from the provided zip file structure and presents it in a user-friendly interface.

## Features

- **Subject Organization**: Content is organized by subject and topics
- **PDF Viewing**: Direct in-browser viewing of PDF files
- **Search Functionality**: Search for specific topics or files
- **User-Friendly Navigation**: Easy sidebar navigation for finding content

## Prerequisites

- Python 3.7 or higher
- Streamlit
- Internet connection (for Streamlit components)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd alevel-study-resources
   ```

2. Install the required dependencies:
   ```
   pip install streamlit
   ```

3. Set up the application using the provided setup script:
   ```
   python setup.py
   ```
   
   This script will automatically extract the ALEVEL.zip file from the `attached_assets` folder. Make sure the zip file is placed in this folder before running the script.
   
   Alternatively, you can manually extract the zip file:
   ```
   mkdir -p static_content
   unzip attached_assets/ALEVEL.zip -d static_content
   ```

## Running the Application

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

## Usage

1. Use the sidebar navigation to browse through subjects and topics
2. Click on any file to view its contents in the main area
3. Use the search box to find specific topics or files

## File Structure

```
├── app.py                   # Main application file
├── setup.py                 # Setup script for extracting content
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── pdf_handler.py       # PDF display functionality
│   └── zip_handler.py       # Zip file handling functions
├── static_content/          # Extracted content from zip file
│   └── ALEVEL/
│       └── EXAM_MATERIALS/  # Study materials by subject
├── attached_assets/         # Original zip file location
│   └── ALEVEL.zip           # Compressed study materials
├── README.md                # This file
```

## Customization

You can modify the application by editing the `app.py` file. The main parts you might want to customize:

- The page title and icon in the `st.set_page_config()`
- The welcome message in the markdown section
- The static content path (`STATIC_CONTENT_PATH`) if your files are stored elsewhere

## License

[Your License Information]

## Acknowledgments

- Streamlit - For the web application framework
- A Level educational content providers