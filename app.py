import os
import streamlit as st
import requests
from PIL import Image
import io

# Set up OCR.Space API key
OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY", "K85999022988957")  # Replace 'your_api_key_here' with your actual key

# Define the OCR function
def perform_ocr(image):
    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    # Send the request to OCR.Space API
    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"image": img_bytes},
        data={"apikey": OCR_SPACE_API_KEY},
    )
    
    # Check the response and parse the text
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        return "Error: " + result.get("ErrorMessage", "Unknown error")
    
    return result["ParsedResults"][0]["ParsedText"]

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
