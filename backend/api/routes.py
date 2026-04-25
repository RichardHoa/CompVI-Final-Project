from flask import Blueprint, request, jsonify
import shutil
import os
from backend.core.pipeline import process_image

api_blueprint = Blueprint("api", __name__)

# Define the path to the images directory
IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

@api_blueprint.route("/analyze", methods=["POST"])
def analyze_image():
    """
    Endpoint to receive an uploaded image, save it temporarily, and process it 
    through the 6-stage physiognomy pipeline.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.content_type.startswith("image/"):
        return jsonify({"error": "File provided is not an image."}), 400

    # Save the uploaded file to the images directory
    file_location = os.path.join(IMAGES_DIR, file.filename)
    file.save(file_location)

    try:
        # Run the image through the analysis pipeline
        result = process_image(file_location)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

