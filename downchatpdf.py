import streamlit as st
from fpdf import FPDF
import base64
import os
import threading


# Create instance of FPDF class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chat Messages', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


def delete_file_after_delay(file_path, delay):
    def delayed_deletion(file_path):
        os.remove(file_path)

    timer = threading.Timer(delay, delayed_deletion, [file_path])
    timer.start()


# Define a function that takes a list of messages and a file name as parameters
def download_messages(conversation, pdf_file_name):
    # Create a PDF object
    pdf = PDF()
    # Add a page to the PDF
    pdf.add_page()
    # Set the font and size
    pdf.set_font("Arial", size=12)
    # Add a cell
    pdf.multi_cell(0, 10, conversation)
    pdf.write(conversation)
    # Save the PDF file to the local laptop
    pdf.output(pdf_file_name)
    # Make the PDF downloadable
    with open(pdf_file_name, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_download_href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_file_name}">Download PDF file</a>'
    st.sidebar.markdown(pdf_download_href, unsafe_allow_html=True)
    # Delete the file after download, schedule the file to be deleted from the server side after 60 seconds
    delete_file_after_delay(pdf_file_name, 60)

