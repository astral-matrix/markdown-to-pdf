import { create } from "zustand";
import { SpacingOption } from "../lib/api";

interface PDFState {
  // Font settings
  fontFamily: string;
  availableFonts: string[];
  setFontFamily: (fontFamily: string) => void;
  setAvailableFonts: (fonts: string[]) => void;

  // Size settings
  sizeLevel: number;
  setSizeLevel: (level: number) => void;

  // Layout settings
  spacing: SpacingOption;
  autoWidthTables: boolean;
  setSpacing: (spacing: SpacingOption) => void;
  setAutoWidthTables: (auto: boolean) => void;

  // Reset to defaults
  resetToDefaults: () => void;
}

export const usePDFStore = create<PDFState>((set) => ({
  // Font settings
  fontFamily: "Inter",
  availableFonts: ["Inter", "Roboto", "Source Code Pro"],
  setFontFamily: (fontFamily) => set({ fontFamily }),
  setAvailableFonts: (fonts) => set({ availableFonts: fonts }),

  // Size settings
  sizeLevel: 3,
  setSizeLevel: (level) => set({ sizeLevel: level }),

  // Layout settings
  spacing: SpacingOption.DEFAULT,
  autoWidthTables: true,
  setSpacing: (spacing) => set({ spacing }),
  setAutoWidthTables: (auto) => set({ autoWidthTables: auto }),

  // Reset to defaults
  resetToDefaults: () =>
    set({
      fontFamily: "Inter",
      sizeLevel: 3,
      spacing: SpacingOption.DEFAULT,
      autoWidthTables: true,
    }),
}));
