from backend.core.stage1_acquisition import acquire_image
from backend.core.stage2_preprocess import preprocess_image
from backend.core.stage3_detection import detect_face
from backend.core.stage4_landmarks import detect_landmarks
from backend.core.stage5_features import extract_features
from backend.core.stage6_interpret import interpret_features
from backend.utils.visualization import visualize_results

def process_image(image_path: str) -> dict:
    """
    Executes the 6-stage physiognomy pipeline sequentially.
    """
    print(f"Starting pipeline for image: {image_path}")

    # Stage 1: Input Acquisition
    raw_frame = acquire_image(image_path)

    # Stage 2: Image Preprocessing
    processed_frame = preprocess_image(raw_frame)

    # Stage 3: Face Detection
    face_roi = detect_face(processed_frame)

    if not face_roi:
        return {"error": "No face detected in the image."}

    # Stage 4: Facial Landmark Detection
    landmarks = detect_landmarks(processed_frame, face_roi)

    # Stage 5: Geometric Feature Extraction
    features = extract_features(landmarks)

    # Stage 6: Rule-based Feature Interpretation
    interpretation = interpret_features(features)

    # Stage 7: Visualization (optional, for debugging or returning an overlay image)
    # visualize_results(processed_frame, face_roi, landmarks)

    # Compile the final result
    result = {
        "features": features,
        "interpretation": interpretation
    }
    
    return result
