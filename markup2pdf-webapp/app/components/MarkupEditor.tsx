import React, { useEffect, useRef } from "react";
import { cn } from "../lib/utils";

interface MarkupEditorProps {
  value: string;
  onChange: (value: string) => void;
  className?: string;
}

export function MarkupEditor({
  value,
  onChange,
  className,
}: MarkupEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea is removed to maintain fixed height

  return (
    <div className={cn("relative w-full", className)}>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full min-h-[300px] h-[300px] p-4 font-mono text-sm text-gray-900 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none placeholder:text-gray-400"
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
