import React, { memo } from "react";
import { useLayout } from "./FormattingContext";
import { SpacingOption } from "../lib/api";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";

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
          <Label htmlFor="spacing">Spacing</Label>
          <Select
            id="spacing"
            value={spacing}
            onChange={(e) => setSpacing(e.target.value as SpacingOption)}
          >
            <option value={SpacingOption.DEFAULT}>Default</option>
            <option value={SpacingOption.COMPACT}>Compact</option>
            <option value={SpacingOption.SPACIOUS}>Spacious</option>
          </Select>
        </div>

        <div className="flex items-center space-x-2">
          <Switch
            id="auto-width-tables"
            checked={autoWidthTables}
            onChange={(e) => setAutoWidthTables(e.target.checked)}
          />
          <Label htmlFor="auto-width-tables">Auto-width tables</Label>
        </div>
      </div>
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const LayoutPanel = memo(LayoutPanelComponent);
