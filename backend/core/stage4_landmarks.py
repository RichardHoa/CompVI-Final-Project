import numpy as np
import cv2
import os

def detect_landmarks(processed_frame, face_landmarks):
    """
    Stage 4: Facial Landmark Detection & Region Extraction
    Uses MediaPipe landmarks to extract specific regions: face, left eye, right eye, lips.
    Saves cropped regions for visualization/debugging and returns them.
    """
    print("[Stage 4] Extracting facial landmarks and region crops")
    
    raw = processed_frame["raw"]
    gray = processed_frame["gray"]
    edges = processed_frame["edges"]
    
    h, w, _ = raw.shape
    
    def pt(i):
        return np.array([
            int(face_landmarks[i].x * w),
            int(face_landmarks[i].y * h)
        ])
        
    def crop_from_points(points_list, pad=35):
        xs = [pt(i)[0] for i in points_list]
        ys = [pt(i)[1] for i in points_list]
            
        x1 = max(min(xs) - pad, 0)
        x2 = min(max(xs) + pad, w)
        y1 = max(min(ys) - pad, 0)
        y2 = min(max(ys) + pad, h)
        
        crop_img = raw[y1:y2, x1:x2]
        crop_gray = gray[y1:y2, x1:x2]
        crop_edge = edges[y1:y2, x1:x2]
        
        return crop_img, crop_gray, crop_edge, (x1, y1, x2, y2)
        
    FACE_POINTS = [
        10,338,297,332,284,251,389,356,454,
        323,361,288,397,365,379,378,400,377,
        152,148,176,149,150,136,172,58,132,
        93,234,127,162,21,54,103,67,109
    ]
    
    LEFT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]
    RIGHT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
    LIPS = [
        61,146,91,181,84,17,314,405,321,375,291,
        0,37,39,40,185,267,269,270,409
    ]
    NOSE = [1, 2, 6, 98, 327, 168, 197, 195, 5, 4]
    
    face_crops = crop_from_points(FACE_POINTS, pad=15)
    left_eye_crops = crop_from_points(LEFT_EYE, pad=5)
    right_eye_crops = crop_from_points(RIGHT_EYE, pad=5)
    lip_crops = crop_from_points(LIPS, pad=10)
    nose_crops = crop_from_points(NOSE, pad=15)
    
    extraction_dir = os.path.join("Photo", "extraction")
    os.makedirs(extraction_dir, exist_ok=True)
    
    cv2.imwrite(os.path.join(extraction_dir, "face_crop.png"), face_crops[0])
    cv2.imwrite(os.path.join(extraction_dir, "left_eye_crop.png"), left_eye_crops[0])
    cv2.imwrite(os.path.join(extraction_dir, "right_eye_crop.png"), right_eye_crops[0])
    cv2.imwrite(os.path.join(extraction_dir, "lip_crop.png"), lip_crops[0])
    cv2.imwrite(os.path.join(extraction_dir, "nose_crop.png"), nose_crops[0])
    
    extracted_data = {
        "landmarks": face_landmarks,
        "face": face_crops,
        "left_eye": left_eye_crops,
        "right_eye": right_eye_crops,
        "lips": lip_crops,
        "nose": nose_crops,
        "pt_func": pt
    }
    
    return extracted_data
