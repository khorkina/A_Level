"""
PDF handling utilities for the A Level Study Resources application.
"""

import base64
import streamlit as st


def display_pdf(pdf_file_path):
    """
    Display a PDF file in Streamlit.
    
    Args:
        pdf_file_path (str): Path to the PDF file to display
    """
    # Open the PDF file in binary mode
    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embed the PDF viewer
    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="600"
            style="border: none;"
        ></iframe>
    """
    
    # Display the PDF viewer
    st.markdown(pdf_display, unsafe_allow_html=True)


def get_pdf_display_code(pdf_file_path):
    """
    Get the HTML code to display a PDF file.
    
    Args:
        pdf_file_path (str): Path to the PDF file to display
        
    Returns:
        str: HTML code to display the PDF
    """
    # Open the PDF file in binary mode
    with open(pdf_file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Create the HTML code for the PDF viewer
    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="600"
            style="border: none;"
        ></iframe>
    """
    
    return pdf_display