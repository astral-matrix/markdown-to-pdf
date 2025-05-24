# Markup2PDF Backend

Python Flask backend for converting Markdown to PDF.

## Getting Started

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd markup2pdf-backend
   ```

2. Create a virtual environment in backend directory (dir: markup2pdf-backend/ ):

   ```
   # Create virtual environment
   python3 -m venv .venv
   ```

3. Activate the virtual environment (dir: markup2pdf-backend/ ):

   ```
   # On macOS/Linux
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

4. Install dependencies (dir: markup2pdf-backend/ ):

   ```
   python3 -m pip install -r requirements.txt
   ```

5. Test the backend server (dir: markup2pdf-backend/ ):
   ```
   python3 run.py
   ```

The server will run on http://localhost:5000 by default.
