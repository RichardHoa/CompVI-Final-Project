import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import os

def detect_face(processed_frame):
    """
    Stage 3: Face Detection (Tasks API)
    Uses MediaPipe FaceLandmarker with tuned parameters for higher accuracy.
    """
    print("[Stage 3] Detecting face using high-precision MediaPipe model")
    
    # Path to the new high-precision model
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../face_landmarker_heavy.task"))

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1,
        min_face_detection_confidence=0.6,
        min_face_presence_confidence=0.6
    )
    
    with vision.FaceLandmarker.create_from_options(options) as landmarker:
        # Use the pre-processed 'gray' image which has CLAHE, bilateral filtering, and sharpening
        print("[Stage 3] Running detection on processed grayscale image")
        
        # MediaPipe Tasks expects an RGB image, so we convert gray to BGR then RGB
        enhanced_bgr = cv2.cvtColor(processed_frame["gray"], cv2.COLOR_GRAY2BGR)
        enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=enhanced_rgb)
        
        result = landmarker.detect(mp_image)

        if not result.face_landmarks:
            return None
            
        return result.face_landmarks[0]
