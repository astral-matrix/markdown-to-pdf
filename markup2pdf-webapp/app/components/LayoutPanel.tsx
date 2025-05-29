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
  const { spacing, autoWidthTables, setSpacing, setAutoWidthTables } =
    useLayout();

  return (
    <div className="space-y-2 p-4 bg-gray-50 dark:bg-neutral-800 rounded-md shadow">
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
            <SelectContent>
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
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const LayoutPanel = memo(LayoutPanelComponent);
