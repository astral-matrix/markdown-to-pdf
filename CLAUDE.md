# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Markdown to PDF Converter - a monorepo web app that converts ChatGPT markdown to styled PDFs with customizable typography and code syntax highlighting.

## Development Commands

### Backend (Python)
```bash
cd markdown2pdf-backend
source .venv/bin/activate
python3 run.py                    # Start server on http://localhost:8000
```

### Frontend (Next.js)
```bash
cd markdown2pdf-webapp
npm run dev                       # Start dev server on http://localhost:3000
npm run build                     # Production build
npm run lint                      # ESLint
npm run diagrams                  # Regenerate Mermaid diagram SVGs from docs/
```

### Initial Setup
```bash
./install.sh                      # Creates venv, installs all dependencies
```

## Code Quality (Required Before Commits)

All changes must pass these checks:

```bash
# Backend
source markdown2pdf-backend/.venv/bin/activate
mypy app
pylint app

# Frontend
cd markdown2pdf-webapp
npx eslint .
```

## Architecture

```
User → Next.js (port 3000) → FastAPI (port 8000) → PDF
```

### Backend (`markdown2pdf-backend/`)
- **Entry:** `app/main.py` - FastAPI app with CORS for localhost:3000
- **Routes:** `app/api/` - `/generate-pdf`, `/generate-pdf-preview`, `/fonts`
- **Services:** `app/services/`
  - `PDFService` - Orchestrates markdown→HTML→PDF via WeasyPrint
  - `MarkdownService` - CommonMark+GitHub parsing with Pygments highlighting
  - `FontService` - Font registration (15+ fonts in `app/static/fonts/`)
- **Models:** `app/models/pdf_request.py` - Pydantic validation for PDF requests
- **Styling:** `app/static/css/styles.css`, `code-highlight.css`

### Frontend (`markdown2pdf-webapp/`)
- **Entry:** `app/page.tsx` - Sets up providers (Query, DarkMode, Formatting)
- **State:** React Context in `app/context/FormattingContext.tsx` (typography, layout, filename)
- **API:** `app/lib/api.ts` - Backend fetch wrappers
- **Key components:**
  - `MarkdownEditor.tsx` - Markdown input
  - `TypographyPanel.tsx`, `LayoutPanel.tsx` - Formatting controls
  - `PDFPreview.tsx` - Live HTML preview (throttled to 2s)
  - `GenerateButton.tsx`, `PDFActions.tsx` - PDF generation/download
- **UI:** shadcn/ui components (Radix primitives) + TailwindCSS

### Key Patterns
- Services exported as singletons from `services/__init__.py`
- Multiple React contexts to optimize re-renders
- Preview API calls throttled via `useThrottledPreview` hook
- TypeScript types in `app/lib/api.ts` must match Pydantic models
