# Importing required libraries
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from the Gemini model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process the uploaded PDF file and extract content
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Configuration
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

# Set a background color and style using Streamlit's Markdown and CSS
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f9;  /* Light gray background */
            color: #333333;  /* Dark text for readability */
            font-family: 'Arial', sans-serif;
        }
        .main-header {
            background-color: #5a5cdd;  /* Soft purple header */
            color: white;
            padding: 20px;
            border-radius: 10px;
        }
        .subheader {
            color: #5a5cdd;  /* Matching subheader color */
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;  /* Sidebar light gray */
        }
        .stButton > button {
            background-color: #5a5cdd;  /* Soft purple buttons */
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #4a4ac7;  /* Darker purple on hover */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header Section
st.markdown('<div class="main-header"><h1>ATS Resume Expert</h1></div>', unsafe_allow_html=True)
st.markdown('<h3 class="subheader">Optimize Your Resume for Job Applications</h3>', unsafe_allow_html=True)

# Input text area for job description
st.write("### Enter the Job Description:")
input_text = st.text_area("Paste the job description below", key="input")

# File uploader for uploading resumes in PDF format
st.write("### Upload Your Resume:")
uploaded_file = st.file_uploader("Supported file types: PDF", type=["pdf"])

# Buttons for user actions in a horizontal layout
col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("Evaluate Resume")
with col2:
    submit3 = st.button("Get Percentage Match")

# Prompts for AI evaluation
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume aligns 
with the job description. The output should include the percentage, missing keywords, and final thoughts.
"""

# Processing actions based on button clicks
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.success("Your Resume Evaluation Results:")
        st.write(response)
    else:
        st.error("Please upload a resume.")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.success("Percentage Match Results:")
        st.write(response)
    else:
        st.error("Please upload a resume.")

# Footer with branding or credits
st.markdown(
    """
    ---
    <div style="text-align: center; color: #888888;">
        <small>Powered by Streamlit & Google Generative AI | Designed by <strong>You</strong></small>
    </div>
    """,
    unsafe_allow_html=True,
)
