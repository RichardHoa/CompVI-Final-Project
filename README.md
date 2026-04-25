# Physiognomy Analysis System (Nhân tướng học)

## System Pipeline
The system follows a sequential pipeline of six stages, transforming raw visual input into analyzed facial feature output.

1. **Input Acquisition**
   - **Source:** webcam stream or uploaded image/video file
   - **Tool:** OpenCV (`cv2.VideoCapture` / `cv2.imread`)
   - **Output:** raw frame in RGB/BGR format

2. **Image Preprocessing**
   - Resize frame to a fixed resolution (e.g. 640×480)
   - Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for lighting normalization
   - Apply Gaussian Blur for noise reduction
   - **Output:** cleaned, normalized frame ready for detection

3. **Face Detection**
   - **Model:** MTCNN, RetinaFace, or HaarCascade
   - **Output:** bounding box coordinates of detected face region (ROI)

4. **Facial Landmark Detection**
   - **Model:** MediaPipe Face Mesh (468 keypoints) or Dlib (68 keypoints)
   - **Output:** array of (x, y) coordinates mapping key facial structures — eyes, nose, mouth, jawline, and eyebrows

5. **Geometric Feature Extraction**
   - Compute facial metrics from landmark coordinates, including:
     - Face ratio (length / width)
     - Inter-ocular distance (distance between eyes)
     - Nose width
     - Mouth width ratio
     - Jaw angle
   - **Output:** numerical feature vector representing facial geometry

6. **Visualization & Output**
   - Render bounding box and landmark points over the original frame
   - Display computed metrics and interpretation results via web UI (HTML/JS frontend + FastAPI backend)

## Setup & Installation Instructions

Follow these steps to run the basic application mock.

### Running the Application
Make sure you have Python 3.8+ installed.

1. **Navigate to the project root:**
   ```bash
   cd path/to/CompVI-Final-Project
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server:**
   ```bash
   python3 backend/main.py
   ```
   The application will start running at `http://localhost:4000`.

5. **Test the Pipeline:**
   - Open your browser and navigate to `http://localhost:4000`.
   - Upload any image file using the UI.
   - Click "Analyze Image".
   - The backend pipeline will run and return results on your screen.

---