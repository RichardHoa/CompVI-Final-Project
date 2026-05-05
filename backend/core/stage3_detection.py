import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import os

def detect_face(processed_frame):
    """
    Stage 3: Face Detection (Tasks API)
    Uses MediaPipe FaceLandmarker to detect landmarks.
    """
    print("[Stage 3] Detecting face using MediaPipe Tasks FaceLandmarker")
    
    # Path to the model file in the project root
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../face_landmarker_v2_with_blendshapes.task"))
    
    if not os.path.exists(model_path):
        # Try relative to CWD just in case
        model_path = "face_landmarker_v2_with_blendshapes.task"

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
    
    with vision.FaceLandmarker.create_from_options(options) as landmarker:
        # MediaPipe Tasks expects mp.Image
        rgb = cv2.cvtColor(processed_frame["raw"], cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        result = landmarker.detect(mp_image)
        
        if not result.face_landmarks:
            return None
            
        # Return the first face's landmarks
        return result.face_landmarks[0]
