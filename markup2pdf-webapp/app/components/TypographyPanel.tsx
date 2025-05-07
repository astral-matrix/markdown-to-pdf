import React from "react";
import { usePDFStore } from "../store/pdfStore";
import { sizeLevelToName } from "../lib/utils";

export function TypographyPanel() {
  const { fontFamily, availableFonts, sizeLevel, setFontFamily, setSizeLevel } =
    usePDFStore();

  return (
    <div className="space-y-4 p-4 bg-gray-50 rounded-md">
      <h2 className="text-xl font-bold text-gray-900 pb-2 border-b border-gray-200">
        Typography
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <label
            htmlFor="font-family"
            className="block text-sm font-medium text-gray-700"
          >
            Font Family
          </label>
          <select
            id="font-family"
            value={fontFamily}
            onChange={(e) => setFontFamily(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
            className="block text-sm font-medium text-gray-700"
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
            <span className="text-sm font-medium w-32 text-gray-900">
              {sizeLevelToName(sizeLevel)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
