import os
from flask import Flask, request, render_template
from PIL import Image
import pytesseract

app = Flask(__name__)

# Configure Tesseract path if necessary
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

@app.route('/', methods=['GET', 'POST'])
def index():
    recognized_text = ""
    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Save the uploaded file
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Perform OCR on the image``
            recognized_text = perform_ocr(file_path)
            
            # Clean up the saved file
            os.remove(file_path)
            
    return render_template('index.html', recognized_text=recognized_text)

def perform_ocr(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    return text

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)  # Create uploads directory if not exists
    app.run(debug=True)
