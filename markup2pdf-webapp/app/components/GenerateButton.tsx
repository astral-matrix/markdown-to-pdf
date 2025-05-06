import React from "react";
import { useMutation } from "@tanstack/react-query";
import { api, PDFGenerationRequest } from "../lib/api";
import { savePDF, getTimestampForFilename } from "../lib/utils";

interface GenerateButtonProps {
  request: PDFGenerationRequest;
  disabled?: boolean;
}

export function GenerateButton({
  request,
  disabled = false,
}: GenerateButtonProps) {
  const generatePdfMutation = useMutation({
    mutationFn: api.generatePDF,
    onSuccess: (data) => {
      // Save the PDF with a timestamp in the filename
      const timestamp = getTimestampForFilename();
      savePDF(data, `document-${timestamp}.pdf`);
    },
  });

  const isLoading = generatePdfMutation.isPending;
  const hasError = generatePdfMutation.isError;

  return (
    <div className="space-y-2">
      <button
        onClick={() => generatePdfMutation.mutate(request)}
        disabled={disabled || isLoading}
        className={`w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md flex items-center justify-center transition-colors
          ${disabled || isLoading ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        {isLoading ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Generating PDF...
          </>
        ) : (
          "Generate PDF"
        )}
      </button>

      {hasError && (
        <div className="text-red-500 text-sm text-center">
          Error generating PDF. Please try again.
        </div>
      )}
    </div>
  );
}
