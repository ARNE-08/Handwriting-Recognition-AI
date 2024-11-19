# Handwriting-Recognition-AI

This project implements a handwriting recognition system using YOLO models. The process involves detecting words in a handwritten image using a word detection model and then detecting individual letters within each word using a letter detection model. The system leverages Flask for a user-friendly web interface and integrates Roboflow's YOLO models for detection tasks.

Features
- Word Detection: A YOLO-based model detects words in the uploaded handwritten image.
- Letter Detection: Another YOLO-based model detects individual letters within the cropped words.
- Flask Integration: Provides a simple web interface for uploading images and viewing results.

## How It Works
- Image Upload: Users upload a handwritten image through the web interface.
- Word Detection:
The word detection YOLO model identifies bounding boxes for each word in the image.
Each detected word is cropped and saved for further processing.
- Letter Detection:
The cropped word images are passed to the letter detection YOLO model.
Letters are detected within each cropped word, and the results are sorted by position to reconstruct the word.
- Output:
The detected words are combined into a complete sentence or paragraph.
The recognized text is displayed on the web interface.
