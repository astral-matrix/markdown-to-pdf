import React, { useState, useCallback, memo, useEffect } from "react";
import { useFilename } from "./FormattingContext";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";

interface FilenameInputProps {
  className?: string;
}

function FilenameInputComponent({ className }: FilenameInputProps) {
  const { filename, setFilename } = useFilename();
  const [localFilename, setLocalFilename] = useState(filename);

  // Set up debouncing - only update the global state after typing stops for 300ms
  useEffect(() => {
    const timer = setTimeout(() => {
      if (localFilename !== filename) {
        setFilename(localFilename);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [localFilename, setFilename, filename]);

  // Handle local state change without updating the global state immediately
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalFilename(e.target.value);
  }, []);

  return (
    <div className={className}>
      <Label
        htmlFor="filename"
        className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
      >
        Filename (optional)
      </Label>
      <Input
        type="text"
        id="filename"
        name="filename"
        placeholder="Optional filename"
        value={localFilename}
        onChange={handleChange}
        className="h-10"
      />
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const FilenameInput = memo(FilenameInputComponent);
