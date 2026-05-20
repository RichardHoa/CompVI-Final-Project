# Physiognomy Analysis System (Face Reading)

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

## Preprocessing & Detection Pipeline Parameters (Stage 2 & Stage 3)

Below is a flat list of all image transformations and detector configurations used in the preprocessing and face detection stages, along with their parameters and technical justifications:

*   **Grayscale Conversion**: params used: `cv2.COLOR_BGR2GRAY`. Eliminates color and skin tone variations, reducing the input to a single intensity channel. This saves processing bandwidth and focuses subsequent operations purely on spatial and structural boundaries. Using other color spaces (e.g., HSV or YCrCb) is avoided because geometric landmark detection relies on spatial contours rather than chrominance.
*   **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: params used: `clipLimit=2.0`, `tileGridSize=(8,8)`. Normalizes uneven lighting locally (like side-shadows) without washing out global details. A `clipLimit` of `2.0` prevents over-amplifying noise in homogeneous regions (which occurs at values > 3.0), while a `tileGridSize` of `(8,8)` is small enough to adjust local brightness cells without producing blocky boundary artifacts.
*   **Bilateral Filtering**: params used: `d=9`, `sigmaColor=75`, `sigmaSpace=75`. Smooths out fine skin textures, pores, and sensor noise while keeping key boundaries (eyes, nose, lips) sharp. A neighborhood diameter of `9` provides sufficient noise smoothing with reasonable computation latency. Selecting values below `50` fails to smooth skin noise, whereas values above `100` begin blending distinct facial boundaries together.
*   **Gaussian Blur**: params used: `kernel=(0,0)`, `sigmaX=3`. Generates a low-pass blurred frame for the unsharp masking algorithm. A sigma of `3` focuses on mid-frequency facial contours rather than high-frequency noise. Setting the kernel to `(0,0)` lets OpenCV calculate the ideal kernel size dynamically from the sigma value, avoiding manual hardcoding.
*   **Unsharp Masking (addWeighted)**: params used: `alpha=1.5`, `beta=-0.5`, `gamma=0`. Sharpens structural contours (like the eye crease or nose bridge) by subtracting a fraction of the blurred image from the original. The weights `1.5` and `-0.5` are standard high-boost scaling parameters that maximize feature contrast without introducing excessive ringing artifacts or high-frequency speckles.
*   **Canny Edge Detection**: params used: `threshold1=20`, `threshold2=80`. Extracts structural edge lines. Standard edge thresholds (e.g., `100` and `200`) are designed for high-contrast object silhouettes and fail to capture subtle interior facial details like nose folds and lip outlines. Lowering thresholds to `20` and `80` ensures these fine structures are captured while maintaining a sufficient ratio to prevent ambient noise from cluttering the edge map.
*   **Morphological Closing**: params used: `kernel=np.ones((3,3))`, `op=cv2.MORPH_CLOSE`. Fills in small 1-2 pixel gaps in detected Canny edges to produce continuous lines. The small `3x3` kernel size is selected because larger kernels (e.g. `5x5` or `7x7`) would merge distinct neighboring features (like lips and chin) together, while smaller kernels would fail to bridge the gaps.
*   **MediaPipe Model Asset**: params used: `face_landmarker_heavy.task`. Employs a high-capacity model designed for sub-pixel landmark precision. While lighter versions (e.g. `lite` or `detector`) are faster, they suffer from coordinate jitter that makes geometric ratio calculations (like eye aspect ratios or lip thickness) highly unstable and inaccurate.
*   **MediaPipe Face Count**: params used: `num_faces=1`. Restricts the detection engine to a single target face. Allowing multiple faces would cause computational overhead and introduce ambiguity in individual physiognomy reporting if bystanders are present.
*   **MediaPipe Detection Confidence**: params used: `min_face_detection_confidence=0.6`. Balances face acquisition sensitivity and false detection avoidance. Raising it (e.g. `0.8`) causes detection failure on slightly turned or low-contrast faces, while lowering it (e.g. `0.3`) risk generating false face meshes on background textures or object patterns.
*   **MediaPipe Presence Confidence**: params used: `min_face_presence_confidence=0.6`. Governs the model's threshold for keeping track of the face mesh once initialized. Setting this to `0.6` prevents the landmarks from shifting or snapping onto non-face pixels in successive frames or slightly occluded views, maintaining measurement reliability without causing early dropouts.