from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from backend.core.pipeline import process_image

api_blueprint = Blueprint("api", __name__)

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}

def _is_allowed_file(filename: str, content_type: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return content_type.startswith("image/") or ext in ALLOWED_EXTENSIONS

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

    if not _is_allowed_file(file.filename, file.content_type):
        return jsonify({"error": "File provided is not a supported image format."}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": "Invalid filename."}), 400

    # Save the uploaded file to the images directory
    file_location = os.path.join(IMAGES_DIR, filename)
    file.save(file_location)

    try:
        # Run the image through the analysis pipeline
        result = process_image(file_location)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

