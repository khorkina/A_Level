import streamlit as st
import os
import base64

def display_pdf(pdf_file_path):
    """
    Display a PDF file in Streamlit.
    
    Args:
        pdf_file_path (str): Path to the PDF file to display
    """
    try:
        # Check if file exists
        if not os.path.exists(pdf_file_path):
            st.error(f"File not found: {pdf_file_path}")
            return
        
        # Display PDF using iframe
        with open(pdf_file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Embed PDF viewer
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Provide download button
        with open(pdf_file_path, "rb") as file:
            btn = st.download_button(
                label="Download PDF",
                data=file,
                file_name=os.path.basename(pdf_file_path),
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")
