import React from "react";
import { PDFGenerationRequest } from "../lib/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface PDFPreviewProps {
  request: PDFGenerationRequest;
}

export function PDFPreview({ request }: PDFPreviewProps) {
  const isMarkupEmpty = !request.markup.trim();

  return (
    <div className="border rounded-md shadow-sm bg-white overflow-auto">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold text-gray-900">PDF Preview</h2>
      </div>

      <div className="p-4 min-h-[300px]">
        {isMarkupEmpty ? (
          <p className="text-gray-400 italic">
            Enter some markdown content to see a preview
          </p>
        ) : (
          <article className="prose prose-sm sm:prose max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {request.markup}
            </ReactMarkdown>
          </article>
        )}
      </div>
    </div>
  );
}
