"use client";

import { useState, useEffect, useMemo } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MarkupEditor } from "./components/MarkupEditor";
import { TypographyPanel } from "./components/TypographyPanel";
import { LayoutPanel } from "./components/LayoutPanel";
import { PDFPreview } from "./components/PDFPreview";
import {
  FormattingProvider,
  useTypography,
  useLayout,
} from "./components/FormattingContext";
import { api, PDFGenerationRequest } from "./lib/api";
import { PDFActions } from "./components/PDFActions";
import { DarkModeProvider } from "./components/DarkModeProvider";
import { DarkModeToggle } from "./components/DarkModeToggle";

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
      <DarkModeProvider>
        <FormattingProvider>
          <EditorPage />
        </FormattingProvider>
      </DarkModeProvider>
    </QueryClientProvider>
  );
}

function EditorPage() {
  const [markup, setMarkup] = useState<string>("");
  const { setAvailableFonts, fontFamily, sizeLevel } = useTypography();
  const { spacing, autoWidthTables } = useLayout();

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

  // Create PDF generation request - memoized to prevent unnecessary recreations
  const pdfRequest: PDFGenerationRequest = useMemo(
    () => ({
      markup,
      font_family: fontFamily,
      size_level: sizeLevel,
      spacing,
      auto_width_tables: autoWidthTables,
    }),
    [markup, fontFamily, sizeLevel, spacing, autoWidthTables]
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-neutral-900 dark:to-neutral-800 flex flex-col text-gray-900 dark:text-gray-100">
      <header className="bg-gray-50 dark:bg-neutral-900 shadow border dark:border-neutral-800">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Markdown to PDF Converter</h1>
          <DarkModeToggle />
        </div>
      </header>

      <main className="flex-grow max-w-7xl mx-auto w-full py-4 px-4 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-4">
          <div className="h-max grid gap-4 lg:col-span-1 min-w-64">
            <TypographyPanel />
            <LayoutPanel />
            <PDFActions markup={markup} />
          </div>

          <div className="space-y-6 lg:col-span-3 ">
            <div className="bg-white dark:bg-neutral-900 shadow rounded-md p-4 border dark:border-neutral-800 ">
              <h2 className="text-xl font-semibold mb-4">Markdown Editor</h2>
              <MarkupEditor value={markup} onChange={setMarkup} />
            </div>
            <div className="bg-white dark:bg-neutral-900 shadow rounded-md">
              <PDFPreview request={pdfRequest} />
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white dark:bg-neutral-900 border-t dark:border-neutral-700 mt-auto">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 dark:text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} Markdown to PDF Converter
          </p>
        </div>
      </footer>
    </div>
  );
}
