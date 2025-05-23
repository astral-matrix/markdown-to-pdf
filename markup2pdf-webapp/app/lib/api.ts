// API endpoint
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

// Types for API requests/responses
export enum SpacingOption {
  DEFAULT = "default",
  COMPACT = "compact",
  SPACIOUS = "spacious",
}

export interface PDFGenerationRequest {
  markup: string;
  font_family?: string;
  size_level?: number;
  spacing?: SpacingOption;
  auto_width_tables?: boolean;
  filename?: string;
}

// API functions
export const api = {
  /**
   * Generate a PDF from markdown
   */
  generatePDF: async (data: PDFGenerationRequest): Promise<Blob> => {
    const response = await fetch(`${API_URL}/generate-pdf`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        errorData?.detail || `Failed to generate PDF: ${response.status}`
      );
    }

    return await response.blob();
  },

  /**
   * Get available font families
   */
  getFonts: async (): Promise<string[]> => {
    const response = await fetch(`${API_URL}/fonts`);

    if (!response.ok) {
      throw new Error(`Failed to fetch fonts: ${response.status}`);
    }

    return await response.json();
  },
};
