# Physiognomy Analysis System (Nhân tướng học)

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