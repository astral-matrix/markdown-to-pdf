import React, { useState, useCallback, memo, useEffect } from "react";
import { useFilename } from "./FormattingContext";

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
      <label
        htmlFor="filename"
        className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
      >
        Filename (optional)
      </label>
      <input
        type="text"
        id="filename"
        name="filename"
        placeholder="Optional filename"
        value={localFilename}
        onChange={handleChange}
        className="block w-96 rounded-md border p-2 h-10 text-gray-900 dark:text-gray-100 bg-white dark:bg-neutral-900 border-gray-300 dark:border-neutral-700 focus:border-blue-500 focus:ring-blue-500"
      />
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const FilenameInput = memo(FilenameInputComponent);
