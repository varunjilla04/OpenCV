import os
from PIL import Image
import pytesseract
import streamlit as st

# Configure Tesseract path if necessary
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

# Define the OCR function
def perform_ocr(image):
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(image)
    return text

# Streamlit app layout and functionality
st.title("Image OCR Application")
st.write("Upload an image to extract text using OCR.")

# Upload the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image with PIL
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Processing...")

    # Perform OCR and display the text
    recognized_text = perform_ocr(image)
    st.write("**Recognized Text:**")
    st.text(recognized_text)
