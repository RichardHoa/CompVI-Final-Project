import math

def extract_features(landmarks):
    """
    Stage 5: Geometric Feature Extraction
    Computes facial metrics from landmark coordinates.
    """
    print("[Stage 5] Extracting geometric features from landmarks")
    
    # Mock mathematical computations based on landmarks
    # Example: inter-ocular distance
    lx, ly = landmarks["left_eye"]
    rx, ry = landmarks["right_eye"]
    inter_ocular_dist = math.hypot(rx - lx, ry - ly)
    
    # Mocking a set of computed features
    mock_features = {
        "face_ratio": 1.45,
        "inter_ocular_distance": inter_ocular_dist,
        "nose_width": 45.0,
        "mouth_width_ratio": 0.35,
        "jaw_angle": 120.0
    }
    
    return mock_features
