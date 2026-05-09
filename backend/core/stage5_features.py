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
    # Thirds Features
    # ---------------------------
    forehead_center = pt(10)
    left_brow = pt(105)
    right_brow = pt(334)
    brow_center = (left_brow + right_brow) / 2
    nose_base = pt(2)
    chin = pt(152)

    forehead_to_brow = abs(brow_center[1] - forehead_center[1])
    estimated_hairline_y = forehead_center[1] - forehead_to_brow * 1.2

    upper_third = abs(brow_center[1] - estimated_hairline_y)
    middle_third = abs(nose_base[1] - brow_center[1])
    lower_third = abs(chin[1] - nose_base[1])
    total_thirds = upper_third + middle_third + lower_third

    upper_ratio = float(upper_third / total_thirds) if total_thirds > 0 else 0.0
    middle_ratio = float(middle_third / total_thirds) if total_thirds > 0 else 0.0
    lower_ratio = float(lower_third / total_thirds) if total_thirds > 0 else 0.0

    ideal = 1 / 3
    balance_error = abs(upper_ratio - ideal) + abs(middle_ratio - ideal) + abs(lower_ratio - ideal)
    balance_score = max(0.0, 1.0 - balance_error * 1.5)

    # ---------------------------
    # Nose Features
    # ---------------------------
    landmarks = extracted_data["landmarks"]
    left_nostril = pt(98)
    right_nostril = pt(327)
    nose_tip = pt(1)
    bridge_upper = pt(168)
    
    eye_distance = math.hypot(pt(33)[0] - pt(263)[0], pt(33)[1] - pt(263)[1])
    nose_width = math.hypot(left_nostril[0] - right_nostril[0], left_nostril[1] - right_nostril[1])
    nose_length = math.hypot(bridge_upper[0] - nose_tip[0], bridge_upper[1] - nose_tip[1])
    face_height = math.hypot(pt(10)[0] - pt(152)[0], pt(10)[1] - pt(152)[1])

    width_ratio = float(nose_width / eye_distance) if eye_distance > 0 else 0.0
    length_ratio = float(nose_length / face_height) if face_height > 0 else 0.0
    tip_ratio = float(nose_width / nose_length) if nose_length > 0 else 0.0

    bridge_z = landmarks[6].z
    cheek_avg_z = (landmarks[234].z + landmarks[454].z) / 2
    bridge_projection = abs(bridge_z - cheek_avg_z)

    nostril_center_y = (left_nostril[1] + right_nostril[1]) / 2
    tip_offset = nostril_center_y - nose_tip[1]

    # pose error / confidence
    left_cheek_x = landmarks[234].x
    right_cheek_x = landmarks[454].x
    symmetry_pose = abs(left_cheek_x - (1 - right_cheek_x))
    confidence = max(0.0, 1.0 - symmetry_pose * 8.0)

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
        },
        "thirds": {
            "upper_ratio": upper_ratio,
            "middle_ratio": middle_ratio,
            "lower_ratio": lower_ratio,
            "balance_score": balance_score
        },
        "nose": {
            "width_ratio": width_ratio,
            "length_ratio": length_ratio,
            "tip_ratio": tip_ratio,
            "bridge_projection": bridge_projection,
            "tip_offset": float(tip_offset),
            "confidence": confidence
        }
    }
    
    return numeric_features
