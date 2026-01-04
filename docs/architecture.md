# Architecture Overview

This document describes the architecture of the Markdown to PDF converter application—a full-stack system with a React/Next.js frontend and a Python/FastAPI backend.

## High-Level System Architecture

```mermaid
flowchart TB
    subgraph Browser
        User([User])
        UI[Next.js Web App<br/>localhost:3000]
    end

    subgraph Backend[FastAPI Server - localhost:8000]
        API[API Routes]
        PDF[PDFService]
        MD[MarkdownService]
        Font[FontService]
    end

    subgraph Assets[Static Assets]
        CSS[(CSS Stylesheets)]
        Fonts[(Font Files)]
    end

    User -->|Types markdown<br/>Selects options| UI
    UI -->|POST /generate-pdf-preview| API
    UI -->|POST /generate-pdf| API
    UI -->|GET /fonts| API
    API --> PDF
    PDF --> MD
    PDF --> Font
    MD --> CSS
    Font --> Fonts
    PDF -->|HTML or PDF bytes| UI
    UI -->|Renders preview<br/>Downloads PDF| User
```

## Frontend Architecture

The frontend is a Next.js application using React with TypeScript. It uses React Query for API state management and React Context for UI state.

```mermaid
flowchart TB
    subgraph Providers[React Providers]
        QC[QueryClientProvider]
        DM[DarkModeProvider]
        FP[FormattingProvider]
    end

    subgraph Contexts[State Contexts]
        TC[TypographyContext<br/>font, size]
        LC[LayoutContext<br/>spacing, index, breaks]
        FC[FilenameContext]
    end

    subgraph Components[UI Components]
        Page[page.tsx]
        Editor[MarkdownEditor]
        TP[TypographyPanel]
        LP[LayoutPanel]
        Preview[PDFPreview]
        Actions[PDFActions]
        GenBtn[GenerateButton]
    end

    subgraph Hooks[Custom Hooks]
        Throttle[useThrottledPreview]
    end

    subgraph API[API Layer]
        ApiLib[api.ts]
    end

    QC --> DM --> FP
    FP --> TC & LC & FC

    Page --> Editor & TP & LP & Preview & Actions
    Actions --> GenBtn

    TP --> TC
    LP --> LC
    Preview --> Throttle
    Throttle --> ApiLib
    GenBtn --> ApiLib
```

### Key Frontend Components

| Component             | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| `page.tsx`            | Root page, sets up providers and layout             |
| `FormattingContext`   | Manages typography, layout, and filename state      |
| `MarkdownEditor`      | Textarea for markdown input                         |
| `TypographyPanel`     | Font family and size controls                       |
| `LayoutPanel`         | Spacing, table width, index, and page break options |
| `PDFPreview`          | Displays live HTML preview in an iframe             |
| `GenerateButton`      | Triggers PDF generation and download                |
| `useThrottledPreview` | Debounces preview API calls (2s delay)              |

## Backend Architecture

The backend is a FastAPI application that converts Markdown to styled HTML and renders PDFs using WeasyPrint.

```mermaid
flowchart TB
    subgraph API[API Layer]
        Main[main.py<br/>FastAPI App]
        Routes[api/__init__.py]
        PDFRoutes[pdf.py]
        FontRoutes[fonts.py]
    end

    subgraph Models
        Request[PDFGenerationRequest<br/>Pydantic Model]
    end

    subgraph Services
        PDFSvc[PDFService]
        MDSvc[MarkdownService]
        FontSvc[FontService]
    end

    subgraph External
        WP[WeasyPrint]
        RL[ReportLab]
        PyMD[python-markdown]
    end

    subgraph Static[Static Assets]
        StylesCSS[styles.css]
        HighlightCSS[code-highlight.css]
        FontFiles[Font Files TTF/WOFF2]
    end

    Main --> Routes
    Routes --> PDFRoutes & FontRoutes
    PDFRoutes --> Request
    PDFRoutes --> PDFSvc
    FontRoutes --> FontSvc

    PDFSvc --> MDSvc
    PDFSvc --> FontSvc
    PDFSvc --> WP

    MDSvc --> PyMD
    FontSvc --> RL
    FontSvc --> FontFiles

    PDFSvc --> StylesCSS & HighlightCSS
```

### Backend Services

| Service           | Responsibility                                                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `PDFService`      | Orchestrates CSS assembly, calls MarkdownService for HTML, renders PDF via WeasyPrint                                               |
| `MarkdownService` | Converts Markdown to HTML with extensions (tables, fenced code, syntax highlighting), adds heading IDs, generates table of contents |
| `FontService`     | Registers fonts with ReportLab, provides @font-face CSS rules, lists available fonts                                                |

## API Endpoints

| Method | Endpoint                | Description                                 |
| ------ | ----------------------- | ------------------------------------------- |
| `POST` | `/generate-pdf`         | Returns PDF bytes as streaming response     |
| `POST` | `/generate-pdf-preview` | Returns styled HTML for iframe preview      |
| `GET`  | `/fonts`                | Returns list of available font family names |
| `GET`  | `/health`               | Health check endpoint                       |

## Request Flow: Live Preview

```mermaid
sequenceDiagram
    participant User
    participant Editor as MarkdownEditor
    participant Hook as useThrottledPreview
    participant API as api.ts
    participant Backend as FastAPI
    participant PDF as PDFService
    participant MD as MarkdownService
    participant Preview as PDFPreview

    User->>Editor: Types markdown
    Editor->>Hook: request object
    Note over Hook: Debounce 2 seconds
    Hook->>API: generatePDFPreview(request)
    API->>Backend: POST /generate-pdf-preview
    Backend->>PDF: generate_pdf_preview(request)
    PDF->>MD: convert_to_html(markdown, css)
    MD-->>PDF: HTML string
    PDF-->>Backend: Full HTML document
    Backend-->>API: HTML response
    API-->>Hook: HTML string
    Hook->>Preview: onPreviewUpdate(html)
    Preview->>Preview: Write to iframe
```

## Request Flow: PDF Generation

```mermaid
sequenceDiagram
    participant User
    participant Button as GenerateButton
    participant Query as React Query
    participant API as api.ts
    participant Backend as FastAPI
    participant PDF as PDFService
    participant MD as MarkdownService
    participant WP as WeasyPrint

    User->>Button: Click Generate PDF
    Button->>Query: mutate(request)
    Query->>API: generatePDF(request)
    API->>Backend: POST /generate-pdf
    Backend->>PDF: generate_pdf(request)
    PDF->>MD: convert_to_html(markdown, css)
    MD-->>PDF: HTML string
    PDF->>WP: HTML.write_pdf()
    WP-->>PDF: PDF bytes
    PDF-->>Backend: PDF bytes
    Backend-->>API: StreamingResponse
    API-->>Query: Blob
    Query->>Button: onSuccess(blob)
    Button->>User: Download PDF file
```

## Data Model

```mermaid
classDiagram
    class PDFGenerationRequest {
        +string markdown
        +string font_family
        +int size_level
        +SpacingOption spacing
        +bool auto_width_tables
        +string filename
        +bool include_index
        +bool add_page_breaks
    }

    class SpacingOption {
        <<enumeration>>
        DEFAULT
        COMPACT
        SPACIOUS
    }

    PDFGenerationRequest --> SpacingOption
```

## Technology Stack

| Layer         | Technologies                                               |
| ------------- | ---------------------------------------------------------- |
| Frontend      | Next.js 15, React 19, TypeScript, TailwindCSS, React Query |
| Backend       | Python 3.11+, FastAPI, Uvicorn, Pydantic                   |
| PDF Rendering | WeasyPrint                                                 |
| Markdown      | python-markdown with extensions                            |
| Fonts         | ReportLab (registration), custom TTF/WOFF2 files           |
