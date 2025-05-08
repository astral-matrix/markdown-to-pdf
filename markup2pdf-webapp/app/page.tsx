"use client";

import { useState, useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MarkupEditor } from "./components/MarkupEditor";
import { TypographyPanel } from "./components/TypographyPanel";
import { LayoutPanel } from "./components/LayoutPanel";
import { GenerateButton } from "./components/GenerateButton";
import { PDFPreview } from "./components/PDFPreview";
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
  const {
    fontFamily,
    sizeLevel,
    spacing,
    autoWidthTables,
    setAvailableFonts,
    filename,
    setFilename,
  } = usePDFStore();

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
    filename: filename,
  };

  // Handle filename change
  const handleFilenameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilename(e.target.value);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">
            Markup to PDF Converter
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto w-full py-6 px-4 sm:px-6 lg:px-8 flex-grow">
        {/* Formatting Controls */}
        <div className="bg-white shadow-sm rounded-md p-4 mb-6">
          <h2 className="text-xl font-bold text-gray-900 pb-2 border-b border-gray-200 mb-4">
            Formatting Options
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TypographyPanel />
            <LayoutPanel />
          </div>
          {/* Start Generate Button Section */}
          <div className="bg-white  rounded-md p-4 mb-4">
            <div className="flex items-end space-x-4">
              <div>
                <label
                  htmlFor="filename"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Filename (optional)
                </label>
                <input
                  type="text"
                  id="filename"
                  name="filename"
                  placeholder="Optional filename"
                  value={filename}
                  onChange={handleFilenameChange}
                  className="block w-96 rounded-md border p-2 h-10 text-gray-900 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div className="pb-0">
                <GenerateButton
                  request={pdfRequest}
                  disabled={!markup.trim()}
                />
              </div>
            </div>
          </div>
          {/* End Generate Button Section */}
        </div>
        {/* Generate Button Section */}n{/* Editor and Preview Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white shadow-sm rounded-md p-4">
            <h2 className="text-xl font-semibold mb-4 text-gray-900">
              Markdown Editor
            </h2>
            <MarkupEditor value={markup} onChange={setMarkup} />
          </div>

          <div className="bg-white shadow-sm rounded-md">
            <PDFPreview request={pdfRequest} />
          </div>
        </div>
      </main>

      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} Markup to PDF Converter
          </p>
        </div>
      </footer>
    </div>
  );
}
