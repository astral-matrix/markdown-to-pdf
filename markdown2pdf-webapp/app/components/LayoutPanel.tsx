import React, { memo } from "react";
import { useLayout } from "./FormattingContext";
import { SpacingOption } from "../lib/api";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select";
import { Checkbox } from "../../components/ui/checkbox";
import { Label } from "../../components/ui/label";

function LayoutPanelComponent() {
  const {
    spacing,
    autoWidthTables,
    includeIndex,
    addPageBreaks,
    setSpacing,
    setAutoWidthTables,
    setIncludeIndex,
    setAddPageBreaks,
  } = useLayout();

  return (
    <div className="space-y-2 p-4 bg-gray-50 dark:bg-neutral-900 rounded-md shadow border dark:border-neutral-800">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 pb-2 border-b border-gray-200 dark:border-neutral-700">
        Layout
      </h2>

      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <Label
            htmlFor="spacing"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Spacing
          </Label>
          <Select
            value={spacing}
            onValueChange={(value: string) =>
              setSpacing(value as SpacingOption)
            }
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select spacing" />
            </SelectTrigger>
            <SelectContent className="bg-gray-50 dark:bg-neutral-900">
              <SelectItem value={SpacingOption.DEFAULT}>Default</SelectItem>
              <SelectItem value={SpacingOption.COMPACT}>Compact</SelectItem>
              <SelectItem value={SpacingOption.SPACIOUS}>Spacious</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="auto-width-tables"
            checked={autoWidthTables}
            onCheckedChange={(checked: boolean) => setAutoWidthTables(checked)}
          />
          <Label
            htmlFor="auto-width-tables"
            className="text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Auto-width tables
          </Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="include-index"
            checked={includeIndex}
            onCheckedChange={(checked: boolean) => setIncludeIndex(checked)}
          />
          <Label
            htmlFor="include-index"
            className="text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Include index
          </Label>
        </div>

        {/* Conditional "Add page breaks" checkbox - only shows when includeIndex is true */}
        {includeIndex && (
          <div className="flex items-center space-x-2 ml-6">
            <Checkbox
              id="add-page-breaks"
              checked={addPageBreaks}
              onCheckedChange={(checked: boolean) => setAddPageBreaks(checked)}
            />
            <Label
              htmlFor="add-page-breaks"
              className="text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Add page breaks
            </Label>
          </div>
        )}
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const LayoutPanel = memo(LayoutPanelComponent);
