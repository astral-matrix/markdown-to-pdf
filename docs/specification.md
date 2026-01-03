# System Specification

This document captures the primary behaviors, data contracts, and operational flows of the Markdown to PDF application.

## Functional Overview

- Accept Markdown input and typography/layout options from the UI.
- Render a live HTML preview that mirrors the final PDF styling (including fonts and page-break indicators).
- Generate a downloadable PDF with embedded fonts, syntax highlighting, optional table of contents, and optional page breaks before top-level headings.
- Expose available font families to the frontend for selection.

## API Surface (Backend)

### POST `/generate-pdf`
*Request body* — `PDFGenerationRequest`

```json
{
  "markdown": "string (required, non-empty)",
  "font_family": "string (optional, defaults to Inter; validated against available fonts)",
  "size_level": "integer 1..5 (default 3)",
  "spacing": "\"default\" | \"compact\" | \"spacious\" (default \"default\")",
  "auto_width_tables": "boolean (default true)",
  "filename": "string (optional, used for download name)",
  "include_index": "boolean (default false)",
  "add_page_breaks": "boolean (default false; active only if include_index is true)"
}
```

*Behavior*
- Validates Markdown is non-empty and font is supported.
- Registers fonts (lazy).
- Builds CSS (page sizing, font stack, theme styles, optional preview/page-break CSS not used here).
- Converts Markdown → HTML (with nested list handling, glyph sanitization, heading IDs, optional index).
- Renders PDF via WeasyPrint and streams bytes with `Content-Disposition` filename.

### POST `/generate-pdf-preview`
*Request body* — same as `/generate-pdf`.

*Behavior*
- Same HTML generation path as PDF, but:
  - Uses preview-specific font URLs (`/fonts/...`).
  - Appends preview-only CSS to visualize page breaks.
- Returns HTML as `text/html`; frontend injects into iframe.

### GET `/fonts`
*Response* — array of font family strings available for selection and validation.

## Backend Modules

- `app/main.py`: FastAPI app setup, CORS for localhost dev, `/health` endpoint.
- `app/api/pdf.py`: Routes for PDF generation and preview; uses `PDFGenerationRequest`.
- `app/api/fonts.py`: Exposes available font families.
- `app/models/pdf_request.py`: Pydantic model with validators ensuring non-empty Markdown and supported font families.
- `app/services/pdf_service.py`:
  - Registers fonts via `FontService`.
  - Builds CSS (`_build_css`) combining page rules, theme CSS (`styles.css`, `code-highlight.css`), font-face rules, and preview-specific decorations when needed.
  - Converts Markdown to HTML through `MarkdownService`.
  - Renders final PDF with WeasyPrint.
- `app/services/markdown_service.py`:
  - Preprocesses nested lists (normalizes indentation and removes stray blanks).
  - Sanitizes problematic glyphs.
  - Renders Markdown with python-markdown extensions (tables, fenced code, syntax highlighting).
  - Adds heading IDs, optional table of contents page, PDF-friendly wrapping, paragraph spacing, and nested list styling hooks.
- `app/services/font_service.py`:
  - Defines bundled font families and file mappings.
  - Registers fonts with ReportLab, chooses monospace fallback.
  - Supplies `@font-face` rules for preview/PDF and reports available font names.

## Frontend Modules (Next.js / React)

- `app/page.tsx`: Root page composing providers and layout panels, editor, preview, and actions.
- `app/components/FormattingContext.tsx`: Manages typography, layout, and filename state via dedicated contexts with memoized setters.
- `app/components/TypographyPanel.tsx`: Font family selector and size slider.
- `app/components/LayoutPanel.tsx`: Spacing selector, auto-width tables toggle, optional index and page-break toggles.
- `app/components/MarkdownEditor.tsx`: Markdown textarea with starter placeholder text.
- `app/components/PDFPreview.tsx`: Shows HTML preview in an iframe; uses throttled requests to avoid chattiness.
- `app/hooks/useThrottledPreview.ts`: Debounces preview fetches and surfaces cleanup.
- `app/components/PDFActions.tsx`: Wraps filename input and generate button; builds request payload from context values.
- `app/components/GenerateButton.tsx`: React Query mutation to call `/generate-pdf`, saves returned Blob with timestamped filename.
- `app/lib/api.ts`: Fetch helpers for preview, PDF generation, and font listing; shared `PDFGenerationRequest` TypeScript type.
- `app/lib/utils.ts`: Helpers for class names, size labels, filename timestamps, and saving blobs (not modified here but used by components).

## Data Flow (End-to-End)

```mermaid
sequenceDiagram
  participant User
  participant UI as Next.js UI
  participant API as FastAPI API
  participant Services as PDF/Markdown/Font Services
  participant Render as WeasyPrint
\n  User->>UI: Edit Markdown / options\n  UI->>API: POST /generate-pdf-preview\n  API->>Services: Build CSS + fonts, render Markdown → HTML\n  Services-->>UI: HTML preview\n  User->>UI: Click Generate PDF\n  UI->>API: POST /generate-pdf\n  API->>Services: Build CSS + HTML\n  Services->>Render: HTML to PDF bytes\n  Render-->>UI: PDF stream\n  UI-->>User: Download file\n```

## Error Handling & Validation

- Backend raises HTTP 500 on generation failures; logs to stdout (placeholder for real logging).
- Font validation happens in the Pydantic model; unsupported fonts reject the request.
- Frontend disables Generate button when Markdown is empty; preview short-circuits when Markdown is blank.
- React Query mutation surfaces errors via inline message near the button.

## Styling & Assets

- Base CSS: `app/static/css/styles.css` for PDF layout; `code-highlight.css` for syntax highlighting.
- Fonts: Bundled in `app/static/fonts` (backend path) and `markdown2pdf-webapp/public/fonts` (preview path).
- Body CSS derived from size level and spacing; monospace font chosen via `FontService`.

## Performance & UX Considerations

- Preview requests are throttled (2s default) to reduce backend load while typing.
- Font registration is lazy and cached after first use.
- PDF generation attempts direct `write_pdf()` (returns bytes) with a fallback for older WeasyPrint signatures.
*** End Patch
