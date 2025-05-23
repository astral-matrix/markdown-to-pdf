import React, { memo } from "react";
import { useLayout } from "./FormattingContext";
import { SpacingOption } from "../lib/api";

function LayoutPanelComponent() {
  const { spacing, autoWidthTables, setSpacing, setAutoWidthTables } =
    useLayout();

  return (
    <div className="space-y-2 p-4 bg-gray-50 dark:bg-neutral-800 rounded-md shadow">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 pb-2 border-b border-gray-200 dark:border-neutral-700">
        Layout
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <label
            htmlFor="spacing"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Spacing
          </label>
          <select
            id="spacing"
            value={spacing}
            onChange={(e) => setSpacing(e.target.value as SpacingOption)}
            className="w-full p-2 text-sm border border-gray-300 dark:border-neutral-700 rounded-md bg-white dark:bg-neutral-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-neutral-700 rounded"
          />
          <label
            htmlFor="auto-width-tables"
            className="text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Auto-width tables
          </label>
        </div>
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const LayoutPanel = memo(LayoutPanelComponent);
