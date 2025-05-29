import React, { memo } from "react";
import { useTypography } from "./FormattingContext";
import { sizeLevelToName } from "../lib/utils";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select";
import { Slider } from "../../components/ui/slider";
import { Label } from "../../components/ui/label";

function TypographyPanelComponent() {
  const { fontFamily, availableFonts, sizeLevel, setFontFamily, setSizeLevel } =
    useTypography();

  return (
    <div className="space-y-3 p-4 bg-gray-50 dark:bg-neutral-900 rounded-md shadow border dark:border-neutral-800">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 pb-2 border-b border-gray-200 dark:border-neutral-700">
        Typography
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <Label
            htmlFor="font-family"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Font Family
          </Label>
          <Select
            value={fontFamily}
            onValueChange={(value: string) => setFontFamily(value)}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select font family" />
            </SelectTrigger>
            <SelectContent className="bg-gray-50 dark:bg-neutral-900">
              {availableFonts.map((font) => (
                <SelectItem key={font} value={font}>
                  {font}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label
            htmlFor="size-level"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Size Level
          </Label>
          <div className="flex items-center space-x-2">
            <Slider
              value={[sizeLevel]}
              onValueChange={(value: number[]) => setSizeLevel(value[0])}
              min={1}
              max={5}
              step={1}
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
