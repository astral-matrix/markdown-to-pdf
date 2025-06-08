import { useCallback, useRef } from "react";
import { PDFGenerationRequest, api } from "../lib/api";

export const useThrottledPreview = (
  onPreviewUpdate: (html: string) => void,
  delay: number = 2000
) => {
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const onPreviewUpdateRef = useRef(onPreviewUpdate);

  // Keep the callback ref up to date
  onPreviewUpdateRef.current = onPreviewUpdate;

  const throttledGeneratePreview = useCallback(
    (request: PDFGenerationRequest) => {
      // Clear existing timeout
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      // Set new timeout
      timeoutRef.current = setTimeout(async () => {
        try {
          const htmlContent = await api.generatePDFPreview(request);
          onPreviewUpdateRef.current(htmlContent);
        } catch (error) {
          console.error("Failed to generate preview:", error);
          // You could call onPreviewUpdate with an error message here
        }
      }, delay);
    },
    [delay] // Only depend on delay, not on onPreviewUpdate
  );

  // Cleanup function
  const cleanup = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  }, []);

  return { throttledGeneratePreview, cleanup };
};
