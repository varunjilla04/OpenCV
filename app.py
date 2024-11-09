import requests
from PIL import Image
import streamlit as st
from io import BytesIO

# Define the OCR function
def perform_ocr(image):
    # Convert the image to bytes and manually set the file extension
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")  # You can choose "JPEG" or "PNG"
    img_bytes.seek(0)

    # Specify the correct file type
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    # Send the request with the file as bytes and the correct extension
    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"image": ("image.png", img_bytes, "image/png")},  # Explicitly setting the file type
            data={"apikey": "K85999022988957"}
        )
        response.raise_for_status()  # Will raise an exception for a 4xx or 5xx error
        result = response.json()
        
        if result.get("IsErroredOnProcessing"):
            return f"Error: {result.get('ErrorMessage', 'Unknown error')}"
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
