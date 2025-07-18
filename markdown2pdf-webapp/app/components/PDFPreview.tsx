import React, { memo, useState, useEffect, useRef, useCallback } from "react";
import { PDFGenerationRequest } from "../lib/api";
import { useThrottledPreview } from "../hooks/useThrottledPreview";

interface PDFPreviewProps {
  request: PDFGenerationRequest;
}

// Extract only the content needed for preview from the full request
function PDFPreviewComponent({ request }: PDFPreviewProps) {
  const [htmlContent, setHtmlContent] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const isMarkdownEmpty = !request.markdown.trim();

  // Handle preview updates with useCallback to prevent unnecessary re-renders
  const handlePreviewUpdate = useCallback((html: string) => {
    setHtmlContent(html);
    setIsLoading(false);
  }, []);

  // Use throttled preview hook
  const { throttledGeneratePreview, cleanup } = useThrottledPreview(
    handlePreviewUpdate,
    2000 // 2 second delay
  );

  // Trigger preview generation when request changes
  useEffect(() => {
    if (!isMarkdownEmpty) {
      setIsLoading(true);
      throttledGeneratePreview(request);
    } else {
      setHtmlContent("");
      setIsLoading(false);
    }
  }, [
    request.markdown,
    request.font_family,
    request.size_level,
    request.spacing,
    request.auto_width_tables,
    request.include_index,
    isMarkdownEmpty,
    throttledGeneratePreview,
    request,
  ]);

  // Cleanup effect - runs once on unmount
  useEffect(() => {
    return cleanup;
  }, []);

  // Update iframe content when HTML changes
  useEffect(() => {
    if (iframeRef.current && htmlContent) {
      const iframe = iframeRef.current;
      const doc = iframe.contentDocument || iframe.contentWindow?.document;
      if (doc) {
        doc.open();

        // The HTML content from the backend already includes the correct font CSS
        doc.write(htmlContent);
        doc.close();
      }
    }
  }, [htmlContent]);

  return (
    <div className="bg-white dark:bg-neutral-900 shadow rounded-md p-4 border dark:border-neutral-800 ">
      <div className="flex items-baseline mb-4">
        <h2 className="text-xl font-semibold">PDF Preview</h2>
      </div>
      <div className="flex justify-center">
        <div
          className="bg-white shadow-lg relative"
          style={{
            width: "775px",
            height: "900px", // A4 proportions (297/210 * 600)
            maxWidth: "100%",
          }}
        >
          {isMarkdownEmpty ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-400 italic">
                Enter some markdown content to see a preview
              </p>
            </div>
          ) : (
            <>
              <iframe
                ref={iframeRef}
                className={`w-full h-full border-0 transition-opacity duration-300 ${
                  isLoading ? "opacity-0" : "opacity-100"
                }`}
                title="PDF Preview"
                sandbox="allow-same-origin"
                style={{
                  backgroundColor: "white",
                  border: "none",
                  padding: "47px", // 12.5mm = ~47px at 96 DPI
                  boxSizing: "border-box",
                }}
              />
              {isLoading && (
                <div
                  className="absolute inset-0 bg-white flex flex-col items-center"
                  style={{ paddingTop: "200px" }}
                >
                  <div className="flex items-center space-x-2 mb-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    <h2 className="text-gray-600 text-lg font-semibold">
                      Generating preview...
                    </h2>
                  </div>
                  <div className="w-full max-w-md space-y-3 px-12">
                    <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-5/6"></div>
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3"></div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
      {/* </div> */}
    </div>
  );
}

// Use custom equality check to prevent unnecessary re-renders
function arePropsEqual(prevProps: PDFPreviewProps, nextProps: PDFPreviewProps) {
  // Only re-render if markdown content or formatting options change
  // Ignore filename changes as they don't affect the preview
  return (
    prevProps.request.markdown === nextProps.request.markdown &&
    prevProps.request.font_family === nextProps.request.font_family &&
    prevProps.request.size_level === nextProps.request.size_level &&
    prevProps.request.spacing === nextProps.request.spacing &&
    prevProps.request.auto_width_tables ===
      nextProps.request.auto_width_tables &&
    prevProps.request.include_index === nextProps.request.include_index
  );
}

// Export a memoized version of the component with custom comparison
export const PDFPreview = memo(PDFPreviewComponent, arePropsEqual);
