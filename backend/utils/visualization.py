import cv2
import os
import numpy as np

def visualize_results(processed_frame, extracted_data, features):
    """
    Stage 7: Visualization
    Renders bounding boxes, landmark points, and measurement lines over the frame.
    Saves the result to a static directory for user access.
    """
    print("[Stage 7] Visualizing results (Bounding box + Landmarks + Measurements)")
    
    raw_img = processed_frame["raw"].copy()
    h, w, _ = raw_img.shape
    
    # 1. Draw Landmark Dots (all 468)
    landmarks = extracted_data["landmarks"]
    for lm in landmarks:
        px = int(lm.x * w)
        py = int(lm.y * h)
        cv2.circle(raw_img, (px, py), 1, (0, 255, 0), -1)
        
    # 2. Draw ROIs (Face, Eyes, Lips)
    colors = {
        "face": (255, 0, 0),      # Blue
        "left_eye": (0, 255, 255),  # Cyan
        "right_eye": (0, 255, 255), # Cyan
        "lips": (0, 0, 255)       # Red
    }
    
    for region_name, color in colors.items():
        if region_name in extracted_data:
            _, _, _, (x1, y1, x2, y2) = extracted_data[region_name]
            cv2.rectangle(raw_img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(raw_img, region_name.replace("_", " ").title(), (x1, y1-5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # 3. Draw Measurement Lines (Face width markers)
    # Using specific landmarks for accurate visualization
    def draw_measurement(p1_idx, p2_idx, label, color):
        p1 = (int(landmarks[p1_idx].x * w), int(landmarks[p1_idx].y * h))
        p2 = (int(landmarks[p2_idx].x * w), int(landmarks[p2_idx].y * h))
        val = np.linalg.norm(np.array(p1) - np.array(p2))
        
        cv2.line(raw_img, p1, p2, color, 2)
        # Put text near the middle of the line
        mid_x = (p1[0] + p2[0]) // 2
        mid_y = (p1[1] + p2[1]) // 2
        cv2.putText(raw_img, f"{label}: {int(val)}px", (mid_x, mid_y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    draw_measurement(10, 152, "Face Len", (0, 255, 255))   # Yellow-ish/Cyan
    draw_measurement(103, 332, "Forehead W", (255, 255, 0)) # Yellow
    draw_measurement(234, 454, "Cheek W", (255, 255, 0))
    draw_measurement(132, 361, "Jaw W", (255, 255, 0))

    # 4. Save the visualized image
    output_dir = os.path.join("backend", "static", "results")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = "latest_analysis.png"
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, raw_img)
    
    print(f"[Stage 7] Visualization saved to {output_path}")
    return f"/static/results/{filename}"
