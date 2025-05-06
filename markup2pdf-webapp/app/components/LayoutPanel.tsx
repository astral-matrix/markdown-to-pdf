import React from "react";
import { usePDFStore } from "../store/pdfStore";
import { SpacingOption } from "../lib/api";

export function LayoutPanel() {
  const { spacing, autoWidthTables, setSpacing, setAutoWidthTables } =
    usePDFStore();

  return (
    <div className="space-y-4 p-4 bg-gray-50 rounded-md">
      <h2 className="text-lg font-medium">Layout</h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <label
            htmlFor="spacing"
            className="block text-sm font-medium text-gray-700"
          >
            Spacing
          </label>
          <select
            id="spacing"
            value={spacing}
            onChange={(e) => setSpacing(e.target.value as SpacingOption)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={SpacingOption.DEFAULT}>Default</option>
            <option value={SpacingOption.COMPACT}>Compact</option>
            <option value={SpacingOption.SPACIOUS}>Spacious</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="auto-width-tables"
            checked={autoWidthTables}
            onChange={(e) => setAutoWidthTables(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label
            htmlFor="auto-width-tables"
            className="text-sm font-medium text-gray-700"
          >
            Auto-width tables
          </label>
        </div>
      </div>
    </div>
  );
}
