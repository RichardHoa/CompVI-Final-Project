import os
import shutil

from backend.core.stage1_acquisition import acquire_image
from backend.core.stage2_preprocess import preprocess_image
from backend.core.stage3_detection import detect_face
from backend.core.stage4_landmarks import detect_landmarks
from backend.core.stage5_features import extract_features
from backend.core.stage6_interpret import interpret_features
from backend.utils.visualization import visualize_results

STAGES_STATIC_DIR = os.path.join("backend", "static", "stages")

def _copy_stage_images() -> dict:
    os.makedirs(STAGES_STATIC_DIR, exist_ok=True)
    t = f"?t={os.urandom(4).hex()}"

    mappings = [
        (os.path.join("Photo", "preprocess", "gray_enhanced.png"), "gray_enhanced.png"),
        (os.path.join("Photo", "preprocess", "edges.png"),         "edges.png"),
        (os.path.join("Photo", "extraction", "face_crop.png"),     "face_crop.png"),
        (os.path.join("Photo", "extraction", "left_eye_crop.png"), "left_eye_crop.png"),
        (os.path.join("Photo", "extraction", "right_eye_crop.png"),"right_eye_crop.png"),
        (os.path.join("Photo", "extraction", "lip_crop.png"),      "lip_crop.png"),
        (os.path.join("Photo", "extraction", "nose_crop.png"),     "nose_crop.png"),
    ]
    urls = {}
    for src, name in mappings:
        if os.path.exists(src):
            shutil.copy(src, os.path.join(STAGES_STATIC_DIR, name))
            urls[name] = f"/static/stages/{name}{t}"
    return urls

def process_image(image_path: str) -> dict:
    """
    Executes the 6-stage physiognomy pipeline sequentially.
    """
    print(f"Starting pipeline for image: {image_path}")

    raw_frame = acquire_image(image_path)
    processed_frame = preprocess_image(raw_frame)
    face_landmarks = detect_face(processed_frame)

    if not face_landmarks:
        return {"error": "No face detected in the image."}

    extracted_data = detect_landmarks(processed_frame, face_landmarks)
    features = extract_features(extracted_data)
    interpretation = interpret_features(features)
    visualization_url = visualize_results(processed_frame, extracted_data, features)

    stage_images = _copy_stage_images()

    return {
        "features": features,
        "interpretation": interpretation,
        "visualization_url": visualization_url,
        "stage_images": stage_images,
    }
