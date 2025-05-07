"use client";

import { useState, useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MarkupEditor } from "./components/MarkupEditor";
import { PreviewCard } from "./components/PreviewCard";
import { usePDFStore } from "./store/pdfStore";
import { api, PDFGenerationRequest, SpacingOption } from "./lib/api";

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <EditorPage />
    </QueryClientProvider>
  );
}

function EditorPage() {
  const [markup, setMarkup] = useState<string>("");
  const { fontFamily, sizeLevel, spacing, autoWidthTables, setAvailableFonts } =
    usePDFStore();

  // Fetch available fonts on component mount
  useEffect(() => {
    async function fetchFonts() {
      try {
        const fonts = await api.getFonts();
        setAvailableFonts(fonts);
      } catch (error) {
        console.error("Failed to fetch fonts:", error);
      }
    }

    fetchFonts();
  }, [setAvailableFonts]);

  // Create PDF generation request
  const pdfRequest: PDFGenerationRequest = {
    markup,
    font_family: fontFamily,
    size_level: sizeLevel,
    spacing: spacing as SpacingOption,
    auto_width_tables: autoWidthTables,
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">
            Markup to PDF Converter
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white shadow-sm rounded-md p-4">
            <h2 className="text-xl font-semibold mb-4 text-gray-900">
              Markdown Editor
            </h2>
            <MarkupEditor value={markup} onChange={setMarkup} />
          </div>

          <div>
            <PreviewCard request={pdfRequest} />
          </div>
        </div>
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} Markup to PDF Converter
          </p>
        </div>
      </footer>
    </div>
  );
}
