import React from "react";
import { TypographyPanel } from "./TypographyPanel";
import { LayoutPanel } from "./LayoutPanel";
import { GenerateButton } from "./GenerateButton";
import { PDFGenerationRequest } from "../lib/api";

interface PreviewCardProps {
  request: PDFGenerationRequest;
}

export function PreviewCard({ request }: PreviewCardProps) {
  const isMarkupEmpty = !request.markup.trim();

  return (
    <div className="border rounded-md shadow-sm bg-white overflow-hidden">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold text-gray-900">PDF Options</h2>
        <p className="text-gray-500 text-sm mt-1">
          Customize the appearance of your PDF
        </p>
      </div>

      <div className="p-4 space-y-6">
        <TypographyPanel />
        <LayoutPanel />

        <GenerateButton request={request} disabled={isMarkupEmpty} />

        {isMarkupEmpty && (
          <p className="text-amber-600 text-sm text-center">
            Please enter some markdown content to generate a PDF.
          </p>
        )}
      </div>
    </div>
  );
}
