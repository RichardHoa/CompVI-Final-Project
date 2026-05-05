import math
import cv2
import numpy as np

def extract_features(extracted_data):
    """
    Stage 5: Geometric Feature Extraction
    Computes facial metrics from landmark coordinates and region crops.
    """
    print("[Stage 5] Extracting geometric features from landmarks")
    
    pt = extracted_data["pt_func"]
    
    face_img, face_gray, face_edge, face_coords = extracted_data["face"]
    
    # Face length: 10 (top) to 152 (chin)
    face_len = math.hypot(pt(10)[0] - pt(152)[0], pt(10)[1] - pt(152)[1])
    
    # Forehead width: 103 to 332
    forehead_w = math.hypot(pt(103)[0] - pt(332)[0], pt(103)[1] - pt(332)[1])
    
    # Cheek width: 234 to 454
    cheek_w = math.hypot(pt(234)[0] - pt(454)[0], pt(234)[1] - pt(454)[1])
    
    # Jaw width: 132 to 361
    jaw_w = math.hypot(pt(132)[0] - pt(361)[0], pt(132)[1] - pt(361)[1])
    
    L = float(face_len / cheek_w) if cheek_w > 0 else 0.0
    J = float(jaw_w / cheek_w) if cheek_w > 0 else 0.0
    F = float(forehead_w / cheek_w) if cheek_w > 0 else 0.0
    
    left_half = face_img[:, :face_img.shape[1]//2]
    right_half = cv2.flip(face_img[:, face_img.shape[1]//2:], 1)
    min_w = min(left_half.shape[1], right_half.shape[1])
    diff = float(np.mean(np.abs(left_half[:, :min_w].astype("float") - right_half[:, :min_w].astype("float"))))
    
    # ---------------------------
    # Eye Features
    # ---------------------------
    left_eye_img, _, left_eye_edge, _ = extracted_data["left_eye"]
    horizontal_score = int(np.sum(left_eye_edge[:left_eye_edge.shape[0]//2, :] > 0))
    
    eye_w = math.hypot(pt(33)[0] - pt(133)[0], pt(33)[1] - pt(133)[1])
    eye_h = math.hypot(pt(159)[0] - pt(145)[0], pt(159)[1] - pt(145)[1])
    eye_ratio = float(eye_h / eye_w) if eye_w > 0 else 0.0
    
    eye_tilt = math.degrees(math.atan2(pt(133)[1] - pt(33)[1], pt(133)[0] - pt(33)[0]))
    
    face_w = cheek_w
    gap = pt(362)[0] - pt(133)[0]
    gap_ratio = float(gap / face_w) if face_w > 0 else 0.0
    
    # ---------------------------
    # Lip Features
    # ---------------------------
    top_thickness = pt(13)[1] - pt(0)[1]
    bot_thickness = pt(17)[1] - pt(14)[1]
    
    lip_w = pt(267)[0] - pt(37)[0]
    lip_h = pt(17)[1] - pt(0)[1]
    
    lip_ratio = float(lip_h / lip_w) if lip_w > 0 else 0.0
    tb_ratio = float(bot_thickness / top_thickness) if top_thickness > 0 else 0.0
    
    p1 = pt(0)
    p2 = pt(37)
    p3 = pt(267)
    bow_depth = float(p1[1] - min(p2[1], p3[1]))
    
    # ---------------------------
    # Pack Features
    # ---------------------------
    numeric_features = {
        "face": {
            "L": L,
            "J": J,
            "F": F,
            "forehead_w": float(forehead_w),
            "cheek_w": float(cheek_w),
            "jaw_w": float(jaw_w),
            "symmetry_diff": diff
        },
        "eye": {
            "ratio": eye_ratio,
            "tilt": eye_tilt,
            "gap_ratio": gap_ratio,
            "horizontal_score": horizontal_score,
            "eye_height": eye_h
        },
        "lip": {
            "lip_ratio": lip_ratio,
            "tb_ratio": tb_ratio,
            "bow_depth": bow_depth
        }
    }
    
    return numeric_features
