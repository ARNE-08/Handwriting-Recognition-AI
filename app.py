from flask import Flask, render_template, request, redirect, url_for
from roboflow import Roboflow
import cv2
import os
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rf = Roboflow(api_key="5lMKXqFohUNwc7trYqOe")
project_words = rf.workspace().project("text-recognition-zowl1")
project_letters = rf.workspace().project("handwriting-recognition-xyekz")
model_words = project_words.version(3).model
model_letters = project_letters.version(4).model

def sort_predictions_by_yx(predictions, y_threshold=20):
    """
    Sort predictions by y (vertical) and x (horizontal) coordinates.
    """
    predictions.sort(key=lambda pred: (pred['y'], pred['x']))

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

    for row in rows:
        row.sort(key=lambda pred: pred['x'])

    return [pred for row in rows for pred in row]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("preprocessed.png", gray)
    img = cv2.imread("preprocessed.png")

    word_results = model_words.predict(img, confidence=50, overlap=50).json()
    words = word_results['predictions']

    if not words:
        return render_template('result.html', result="No text detected", image_url=file_path)

    sorted_words = sort_predictions_by_yx(words)

    detected_words = []
    for idx, word in enumerate(sorted_words):
        x, y, w, h = word['x'], word['y'], word['width'], word['height']
        x1, y1 = max(0, int(x - w / 2)), max(0, int(y - h / 2))
        x2, y2 = int(x + w / 2), int(y + h / 2)

        word_crop = img[y1:y2, x1:x2] if len(sorted_words) > 1 else img

        letter_results = model_letters.predict(word_crop, confidence=50, overlap=50).json()
        letters = sorted(letter_results['predictions'], key=lambda pred: pred['x'])

        detected_word = ''.join([letter['class'] for letter in letters])
        detected_words.append(detected_word)

    final_result = ' '.join(detected_words)

    return render_template('result.html', result=final_result, image_url=file_path)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
