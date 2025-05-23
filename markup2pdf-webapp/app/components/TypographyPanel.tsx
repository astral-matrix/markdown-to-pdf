import React, { memo } from "react";
import { useTypography } from "./FormattingContext";
import { sizeLevelToName } from "../lib/utils";

function TypographyPanelComponent() {
  const { fontFamily, availableFonts, sizeLevel, setFontFamily, setSizeLevel } =
    useTypography();

  return (
    <div className="space-y-4 p-4 bg-gray-50 dark:bg-neutral-800 rounded-md shadow">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 pb-2 border-b border-gray-200 dark:border-neutral-700">
        Typography
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <label
            htmlFor="font-family"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Font Family
          </label>
          <select
            id="font-family"
            value={fontFamily}
            onChange={(e) => setFontFamily(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 dark:border-neutral-700 rounded-md bg-white dark:bg-neutral-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {availableFonts.map((font) => (
              <option key={font} value={font}>
                {font}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label
            htmlFor="size-level"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Size Level
          </label>
          <div className="flex items-center space-x-2">
            <input
              type="range"
              id="size-level"
              min={1}
              max={5}
              step={1}
              value={sizeLevel}
              onChange={(e) => setSizeLevel(Number(e.target.value))}
              className="w-3/4"
            />
            <span className="text-sm font-medium w-32 text-gray-900 dark:text-gray-100">
              {sizeLevelToName(sizeLevel)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const TypographyPanel = memo(TypographyPanelComponent);
