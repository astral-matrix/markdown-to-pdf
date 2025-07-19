import React, { memo, useMemo } from "react";
import { FilenameInput } from "./FilenameInput";
import { GenerateButton } from "./GenerateButton";
import { PDFGenerationRequest } from "../lib/api";
import { useTypography, useLayout, useFilename } from "./FormattingContext";

interface PDFActionsProps {
  markdown: string;
}

function PDFActionsComponent({ markdown }: PDFActionsProps) {
  // Get values from specific contexts to prevent unnecessary re-renders
  const { fontFamily, sizeLevel } = useTypography();
  const { spacing, autoWidthTables, includeIndex } = useLayout();
  const { filename } = useFilename();

  // Memoize the PDF request object to prevent unnecessary re-creation
  const pdfRequest: PDFGenerationRequest = useMemo(
    () => ({
      markdown,
      font_family: fontFamily,
      size_level: sizeLevel,
      spacing,
      auto_width_tables: autoWidthTables,
      include_index: includeIndex,
      filename,
    }),
    [
      markdown,
      fontFamily,
      sizeLevel,
      spacing,
      autoWidthTables,
      includeIndex,
      filename,
    ]
  );

  return (
    <div className="bg-white dark:bg-neutral-900 rounded-md shadow p-4 min-w-64 border dark:border-neutral-800 ">
      <div className="flex items-end space-x-4">
        <FilenameInput />
      </div>
      <div className="flex justify-end items-end space-x-4 pt-4">
        <GenerateButton request={pdfRequest} disabled={!markdown.trim()} />
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const PDFActions = memo(PDFActionsComponent);
