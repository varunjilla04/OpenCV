import os
import io
import requests
from PIL import Image
import pytesseract
import streamlit as st

# Configure Tesseract path if necessary
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

# Define the OCR function
def perform_ocr(image):
    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    # Send the request to OCR.Space API
    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"image": img_bytes},
            data={"apikey": "YOUR_API_KEY_HERE"}  # Replace with your actual API key
        )
        response.raise_for_status()  # Check for HTTP errors

        # Check the API response
        result = response.json()

        # If OCR failed or the response is in an unexpected format, handle it
        if result.get("IsErroredOnProcessing"):
            error_message = result.get("ErrorMessage", "Unknown error")
            return f"Error: {error_message}"

        # Return parsed text if no error
        return result["ParsedResults"][0]["ParsedText"]
    
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

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
