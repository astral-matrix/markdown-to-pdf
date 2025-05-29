import * as React from "react";
import { cn } from "@/app/lib/utils";

export type SliderProps = React.InputHTMLAttributes<HTMLInputElement>;

export const Slider = React.forwardRef<HTMLInputElement, SliderProps>(
  ({ className, ...props }, ref) => (
    <input
      type="range"
      ref={ref}
      className={cn("w-full h-2 bg-muted rounded-lg cursor-pointer", className)}
      {...props}
    />
  )
);
Slider.displayName = "Slider";
