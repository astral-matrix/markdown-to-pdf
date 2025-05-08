import React, { memo, useMemo } from "react";
import { FilenameInput } from "./FilenameInput";
import { GenerateButton } from "./GenerateButton";
import { PDFGenerationRequest } from "../lib/api";
import { usePDFStore } from "../store/pdfStore";

interface PDFActionsProps {
  markup: string;
}

function PDFActionsComponent({ markup }: PDFActionsProps) {
  // Only access store values needed for the PDF request
  // Explicitly NOT subscribing to filename changes - that's handled by FilenameInput
  const { fontFamily, sizeLevel, spacing, autoWidthTables } = usePDFStore(
    (state) => ({
      fontFamily: state.fontFamily,
      sizeLevel: state.sizeLevel,
      spacing: state.spacing,
      autoWidthTables: state.autoWidthTables,
    })
  );

  // Get filename separately so this component doesn't re-render when filename changes
  const filename = usePDFStore((state) => state.filename);

  // Memoize the PDF request object to prevent unnecessary re-creation
  const pdfRequest: PDFGenerationRequest = useMemo(
    () => ({
      markup,
      font_family: fontFamily,
      size_level: sizeLevel,
      spacing,
      auto_width_tables: autoWidthTables,
      filename,
    }),
    [markup, fontFamily, sizeLevel, spacing, autoWidthTables, filename]
  );

  return (
    <div className="bg-white rounded-md p-4 mb-4">
      <div className="flex items-end space-x-4">
        <FilenameInput />
        <div className="pb-0">
          <GenerateButton request={pdfRequest} disabled={!markup.trim()} />
        </div>
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const PDFActions = memo(PDFActionsComponent);
