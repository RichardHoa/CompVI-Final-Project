import cv2
import os

def acquire_image(source_path: str):
    """
    Stage 1: Input Acquisition
    Reads an image from a file path and saves a copy to the Photo/upload directory.
    """
    print(f"[Stage 1] Acquiring image from {source_path}")
    
    img = cv2.imread(source_path)
    if img is None:
        raise ValueError(f"Cannot read image from {source_path}")
    
    # Save to Photo/upload/
    upload_dir = os.path.join("Photo", "upload")
    os.makedirs(upload_dir, exist_ok=True)
    
    filename = os.path.basename(source_path)
    save_path = os.path.join(upload_dir, filename)
    cv2.imwrite(save_path, img)
    
    return img
