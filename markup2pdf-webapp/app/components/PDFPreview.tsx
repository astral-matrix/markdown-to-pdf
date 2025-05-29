import React, { memo, useMemo } from "react";
import { PDFGenerationRequest } from "../lib/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface PDFPreviewProps {
  request: PDFGenerationRequest;
}

// Extract only the content needed for preview from the full request
function PDFPreviewComponent({ request }: PDFPreviewProps) {
  const isMarkupEmpty = !request.markup.trim();

  // Memoize the markdown content to prevent re-renders when request reference changes
  // but the actual markup content and styling values remain the same
  const markdownContent = useMemo(() => {
    if (isMarkupEmpty) {
      return null;
    }

    return (
      <article className="prose prose-sm sm:prose max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {request.markup}
        </ReactMarkdown>
      </article>
    );
  }, [
    request.markup,
    request.font_family,
    request.size_level,
    request.spacing,
    isMarkupEmpty,
  ]);

  return (
    <div className="pdf-preview border rounded-md shadow-sm bg-white overflow-auto">
      <div className="p-4 border-b border-gray-200 dark:border-neutral-500">
        <h2 className="text-xl font-semibold text-gray-900">PDF Preview</h2>
      </div>

      <div className="p-4 min-h-[500px]">
        {isMarkupEmpty ? (
          <p className="text-gray-400 italic">
            Enter some markdown content to see a preview
          </p>
        ) : (
          markdownContent
        )}
      </div>
    </div>
  );
}

// Use custom equality check to prevent unnecessary re-renders
function arePropsEqual(prevProps: PDFPreviewProps, nextProps: PDFPreviewProps) {
  // Only re-render if markup content or formatting options change
  // Ignore filename changes as they don't affect the preview
  return (
    prevProps.request.markup === nextProps.request.markup &&
    prevProps.request.font_family === nextProps.request.font_family &&
    prevProps.request.size_level === nextProps.request.size_level &&
    prevProps.request.spacing === nextProps.request.spacing &&
    prevProps.request.auto_width_tables === nextProps.request.auto_width_tables
  );
}

// Export a memoized version of the component with custom comparison
export const PDFPreview = memo(PDFPreviewComponent, arePropsEqual);
