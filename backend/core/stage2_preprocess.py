import cv2
import numpy as np
import os

def preprocess_image(raw_frame):
    """
    Stage 2: Image Preprocessing
    Applies operations like grayscale, CLAHE for lighting normalization, 
    bilateral filtering, Gaussian Blur, and Canny Edge Detection.
    Returns a dictionary of frames needed for later stages.
    """
    print("[Stage 2] Preprocessing image (CLAHE -> Bilateral -> Gaussian Blur -> Canny)")
    
    gray = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    
    blur = cv2.GaussianBlur(gray, (0,0), 3)
    gray = cv2.addWeighted(gray, 1.5, blur, -0.5, 0)
    
    # softer edge thresholds
    edges = cv2.Canny(gray, 20, 80)
    
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Save edges for debugging
    preprocess_dir = os.path.join("Photo", "preprocess")
    os.makedirs(preprocess_dir, exist_ok=True)
    cv2.imwrite(os.path.join(preprocess_dir, "edges.png"), edges)
    cv2.imwrite(os.path.join(preprocess_dir, "gray_enhanced.png"), gray)
    
    processed_frame = {
        "raw": raw_frame,
        "gray": gray,
        "edges": edges
    }
    
    return processed_frame
