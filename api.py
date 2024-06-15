from flask import Flask, request, jsonify
from PIL import Image
import torch
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "custom", path="/home/kiq/Documents/ia_project/new_project/yolov5/yolov5/yolov5s.pt")

@app.route("/check", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    try:
        # Read the image file
        image = Image.open(BytesIO(file.read()))

        # Perform inference
        results = model(image)

        # Extract relevant information from results
        detections = []
        for detection in results.xyxy[0]:  # Assuming batch size is 1
            class_name = model.names[int(detection[-1])]
            confidence = float(detection[-2])
            bbox = detection[:4].tolist()  # Convert bbox to list
            
            # Only consider detections of class 'person'
            if class_name == 'person':
                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": bbox
                })

        if any(detection['confidence'] > 0.8 for detection in detections):
            response = 'Dificilmente um palhaço'
        elif detections:
            response = 'Provavelmente um palhaço'
        else:
            response = "Sem palhaço"

        # Return JSON response
        return jsonify({
            "response": response,
            "detections": detections
        })
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error processing image"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
