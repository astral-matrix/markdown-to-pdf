import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { saveAs } from "file-saver";

/**
 * Combines class names with Tailwind CSS support
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Saves a Blob as a PDF file
 */
export function savePDF(blob: Blob, filename: string = "document.pdf") {
  saveAs(blob, filename);
}

/**
 * Maps a size level (1-5) to a descriptive size name
 */
export function sizeLevelToName(level: number): string {
  const sizeMap: Record<number, string> = {
    1: "X-Small",
    2: "Small",
    3: "Medium",
    4: "Large",
    5: "X-Large",
  };

  return sizeMap[level] || "Medium";
}

/**
 * Gets the current timestamp in YYYY-MM-DD-HHMM format for filenames
 */
export function getTimestampForFilename(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hour = String(now.getHours()).padStart(2, "0");
  const minute = String(now.getMinutes()).padStart(2, "0");

  return `${year}-${month}-${day}-${hour}${minute}`;
}
