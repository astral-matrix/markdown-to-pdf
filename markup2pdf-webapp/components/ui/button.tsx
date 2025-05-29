import * as React from "react";
import { cn } from "@/app/lib/utils";

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:pointer-events-none h-10 px-4 text-sm font-medium",
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
