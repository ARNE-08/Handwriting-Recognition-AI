from flask import Flask, render_template, request, redirect, url_for
from roboflow import Roboflow
import cv2
import os
import numpy as np

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Roboflow setup for two models
rf = Roboflow(api_key="5lMKXqFohUNwc7trYqOe")
project_words = rf.workspace().project("text-recognition-zowl1")
project_letters = rf.workspace().project("handwriting-recognition-xyekz")
model_words = project_words.version(1).model  # Change version as per your setup
model_letters = project_letters.version(4).model  # Change version as per your setup

def sort_predictions_by_yx(predictions, y_threshold=20):
    """
    Sort predictions by y (vertical) and x (horizontal) coordinates.
    """
    # Sort primarily by y, secondarily by x
    predictions.sort(key=lambda pred: (pred['y'], pred['x']))

    # Group predictions into rows based on y_threshold
    rows = []
    current_row = []

    for prediction in predictions:
        if not current_row or abs(prediction['y'] - current_row[-1]['y']) <= y_threshold:
            current_row.append(prediction)
        else:
            rows.append(current_row)
            current_row = [prediction]
    if current_row:
        rows.append(current_row)

    # Sort each row by x
    for row in rows:
        row.sort(key=lambda pred: pred['x'])

    # Flatten the sorted rows into a single list
    return [pred for row in rows for pred in row]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400

    # Save uploaded image
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Load the image
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("preprocessed.png", gray)
    img = cv2.imread("preprocessed.png")

    # Step 1: Detect words in the image using the first model
    word_results = model_words.predict(img, confidence=50, overlap=50).json()
    words = word_results['predictions']

    # Step 2: Sort words by y and x coordinates
    sorted_words = sort_predictions_by_yx(words)

    # Step 3: For each detected word, crop and detect letters using the second model
    detected_words = []
    for word in sorted_words:
        x, y, w, h = word['x'], word['y'], word['width'], word['height']
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)

        # Crop the word from the original image
        word_crop = img[y1:y2, x1:x2]

        # Predict letters in the cropped word
        letter_results = model_letters.predict(word_crop, confidence=50, overlap=50).json()
        letters = sorted(letter_results['predictions'], key=lambda pred: pred['x'])  # Sort by x-coordinate

        # Concatenate letters to form the word
        detected_word = ''.join([letter['class'] for letter in letters])
        detected_words.append(detected_word)

    # Final result: Join all detected words
    final_result = ' '.join(detected_words)

    return render_template('result.html', result=final_result, image_url=file_path)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
