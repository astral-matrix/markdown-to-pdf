import React, { useRef, memo, useCallback } from "react";
import { cn } from "../lib/utils";
import { Textarea } from "@/components/ui/textarea";

interface MarkupEditorProps {
  value: string;
  onChange: (value: string) => void;
  className?: string;
}

function MarkupEditorComponent({
  value,
  onChange,
  className,
}: MarkupEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Memoize the change handler
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      onChange(e.target.value);
    },
    [onChange]
  );

  return (
    <div className={cn("relative w-full", className)}>
      <Textarea
        ref={textareaRef}
        value={value}
        onChange={handleChange}
        className="w-full min-h-[300px] h-[300px] font-mono resize-none"
        placeholder="# Enter your markdown here

## Example Content

This is some **bold** and *italic* text.

- List item 1
- List item 2

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |

```js
console.log('Code block example');
```

> This is a blockquote

        [Link example](https://example.com)"
      />
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export const MarkupEditor = memo(MarkupEditorComponent);
