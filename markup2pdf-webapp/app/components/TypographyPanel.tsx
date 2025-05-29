import React, { memo } from "react";
import { useTypography } from "./FormattingContext";
import { sizeLevelToName } from "../lib/utils";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";

function TypographyPanelComponent() {
  const { fontFamily, availableFonts, sizeLevel, setFontFamily, setSizeLevel } =
    useTypography();

  return (
    <div className="space-y-3 p-4 bg-gray-50 dark:bg-neutral-800 rounded-md shadow">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 pb-2 border-b border-gray-200 dark:border-neutral-700">
        Typography
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <Label htmlFor="font-family">Font Family</Label>
          <Select
            id="font-family"
            value={fontFamily}
            onChange={(e) => setFontFamily(e.target.value)}
          >
            {availableFonts.map((font) => (
              <option key={font} value={font}>
                {font}
              </option>
            ))}
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="size-level">Size Level</Label>
          <div className="flex items-center space-x-2">
            <Slider
              id="size-level"
              min={1}
              max={5}
              step={1}
              value={sizeLevel}
              onChange={(e) => setSizeLevel(Number(e.target.value))}
              className="w-3/4"
            />
            <span className="text-sm font-medium w-32">
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
