# Markup to PDF Converter

A full-stack web application that converts Markdown to beautifully styled PDFs with customizable typography and layout options.

## Project Structure

This is a monorepo containing:

- `markup2pdf-backend`: FastAPI Python service for Markdown-to-PDF conversion
- `markup2pdf-webapp`: Next.js frontend for the web application

## Features

- Convert CommonMark + GitHub-style Markdown to styled PDFs
- Customize font family and size
- Layout options including spacing and table width control
- Fast PDF generation (< 1s for average documents)
- Accessibility tagging for screen readers

## Technology Stack

| Layer      | Technologies Used                                       |
| ---------- | ------------------------------------------------------- |
| Frontend   | Next.js, React, TypeScript, TailwindCSS, TanStack Query |
| Backend    | Python, FastAPI, Uvicorn, Pydantic                      |
| PDF Engine | ReportLab (primary), WeasyPrint (fallback)              |
| Markdown   | markdown-it-py with table and highlight plugins         |

## Getting Started

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd markup2pdf-backend
   ```

2. Create a virtual environment:

   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   ```
   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

4. Install dependencies:

   ```
   python3 -m pip install -r requirements.txt
   ```

5. Run the backend server:
   ```
   python3 run.py
   ```

The backend API will be available at http://localhost:5000.

You can check if the server is running by visiting:

- API documentation: http://localhost:5000/docs
- Health check: http://localhost:5000/health

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd markup2pdf-webapp
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

The frontend will be available at http://localhost:3000.

## API Endpoints

| Method | Path          | Description                             |
| ------ | ------------- | --------------------------------------- |
| POST   | /generate-pdf | Generates a PDF from markdown content   |
| GET    | /fonts        | Returns list of available font families |

## Project Goals

- **User workflow:** Paste markup → choose typography options → generate PDF → download
- **Quality:** Output embeds fonts, avoids missing glyphs, wraps table text, supports accessibility tagging
- **Performance:** Fast generation (< 1s for average documents)
- **Reliability:** Well-tested, graceful error handling

## License

MIT
