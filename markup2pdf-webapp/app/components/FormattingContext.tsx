import React, {
  createContext,
  useContext,
  useState,
  useMemo,
  useCallback,
  ReactNode,
} from "react";
import { SpacingOption } from "../lib/api";

// Define the types for our formatting state
export interface FormattingOptions {
  fontFamily: string;
  availableFonts: string[];
  sizeLevel: number;
  spacing: SpacingOption;
  autoWidthTables: boolean;
  filename: string;
}

// Split into multiple contexts to prevent unnecessary re-renders

// Typography Context
interface TypographyContextType {
  fontFamily: string;
  availableFonts: string[];
  sizeLevel: number;
  setFontFamily: (font: string) => void;
  setAvailableFonts: (fonts: string[]) => void;
  setSizeLevel: (level: number) => void;
}

// Layout Context
interface LayoutContextType {
  spacing: SpacingOption;
  autoWidthTables: boolean;
  setSpacing: (spacing: SpacingOption) => void;
  setAutoWidthTables: (auto: boolean) => void;
}

// Filename Context
interface FilenameContextType {
  filename: string;
  setFilename: (filename: string) => void;
}

// Reset Function Context
interface ResetContextType {
  resetToDefaults: () => void;
}

// Create the contexts with default values
const TypographyContext = createContext<TypographyContextType | undefined>(
  undefined
);
const LayoutContext = createContext<LayoutContextType | undefined>(undefined);
const FilenameContext = createContext<FilenameContextType | undefined>(
  undefined
);
const ResetContext = createContext<ResetContextType | undefined>(undefined);

// Default values
const defaultFormattingOptions: FormattingOptions = {
  fontFamily: "Inter",
  availableFonts: ["Inter", "Roboto", "Source Code Pro"],
  sizeLevel: 3,
  spacing: SpacingOption.DEFAULT,
  autoWidthTables: true,
  filename: "",
};

// Create individual providers
export function FormattingProvider({ children }: { children: ReactNode }) {
  // Use separate state variables for different parts of the state
  const [typography, setTypography] = useState({
    fontFamily: defaultFormattingOptions.fontFamily,
    availableFonts: defaultFormattingOptions.availableFonts,
    sizeLevel: defaultFormattingOptions.sizeLevel,
  });

  const [layout, setLayout] = useState({
    spacing: defaultFormattingOptions.spacing,
    autoWidthTables: defaultFormattingOptions.autoWidthTables,
  });

  const [filename, setFilenameState] = useState(
    defaultFormattingOptions.filename
  );

  // Memoized updater functions
  const setFontFamily = useCallback((fontFamily: string) => {
    setTypography((prev) => ({
      ...prev,
      fontFamily,
    }));
  }, []);

  const setAvailableFonts = useCallback((availableFonts: string[]) => {
    setTypography((prev) => ({
      ...prev,
      availableFonts,
    }));
  }, []);

  const setSizeLevel = useCallback((sizeLevel: number) => {
    setTypography((prev) => ({
      ...prev,
      sizeLevel,
    }));
  }, []);

  const setSpacing = useCallback((spacing: SpacingOption) => {
    setLayout((prev) => ({
      ...prev,
      spacing,
    }));
  }, []);

  const setAutoWidthTables = useCallback((autoWidthTables: boolean) => {
    setLayout((prev) => ({
      ...prev,
      autoWidthTables,
    }));
  }, []);

  const setFilename = useCallback((name: string) => {
    setFilenameState(name);
  }, []);

  const resetToDefaults = useCallback(() => {
    setTypography({
      fontFamily: defaultFormattingOptions.fontFamily,
      availableFonts: defaultFormattingOptions.availableFonts,
      sizeLevel: defaultFormattingOptions.sizeLevel,
    });
    setLayout({
      spacing: defaultFormattingOptions.spacing,
      autoWidthTables: defaultFormattingOptions.autoWidthTables,
    });
    setFilenameState(defaultFormattingOptions.filename);
  }, []);

  // Memoize the context values to prevent unnecessary re-renders
  const typographyValue = useMemo(
    () => ({
      ...typography,
      setFontFamily,
      setAvailableFonts,
      setSizeLevel,
    }),
    [typography, setFontFamily, setAvailableFonts, setSizeLevel]
  );

  const layoutValue = useMemo(
    () => ({
      ...layout,
      setSpacing,
      setAutoWidthTables,
    }),
    [layout, setSpacing, setAutoWidthTables]
  );

  const filenameValue = useMemo(
    () => ({
      filename,
      setFilename,
    }),
    [filename, setFilename]
  );

  const resetValue = useMemo(
    () => ({
      resetToDefaults,
    }),
    [resetToDefaults]
  );


  return (
    <ResetContext.Provider value={resetValue}>
      <TypographyContext.Provider value={typographyValue}>
        <LayoutContext.Provider value={layoutValue}>
          <FilenameContext.Provider value={filenameValue}>
            {children}
          </FilenameContext.Provider>
        </LayoutContext.Provider>
      </TypographyContext.Provider>
    </ResetContext.Provider>
  );
}

// Custom hooks to use the contexts
export function useTypography() {
  const context = useContext(TypographyContext);
  if (context === undefined) {
    throw new Error("useTypography must be used within a FormattingProvider");
  }
  return context;
}

export function useLayout() {
  const context = useContext(LayoutContext);
  if (context === undefined) {
    throw new Error("useLayout must be used within a FormattingProvider");
  }
  return context;
}

export function useFilename() {
  const context = useContext(FilenameContext);
  if (context === undefined) {
    throw new Error("useFilename must be used within a FormattingProvider");
  }
  return context;
}

export function useReset() {
  const context = useContext(ResetContext);
  if (context === undefined) {
    throw new Error("useReset must be used within a FormattingProvider");
  }
  return context;
}

// Backward compatibility hook that merges all contexts
export function useFormatting() {
  const typography = useTypography();
  const layout = useLayout();
  const { filename, setFilename } = useFilename();
  const { resetToDefaults } = useReset();

  const options = useMemo(
    () => ({
      fontFamily: typography.fontFamily,
      availableFonts: typography.availableFonts,
      sizeLevel: typography.sizeLevel,
      spacing: layout.spacing,
      autoWidthTables: layout.autoWidthTables,
      filename,
    }),
    [typography, layout, filename]
  );

  return {
    options,
    setFontFamily: typography.setFontFamily,
    setAvailableFonts: typography.setAvailableFonts,
    setSizeLevel: typography.setSizeLevel,
    setSpacing: layout.setSpacing,
    setAutoWidthTables: layout.setAutoWidthTables,
    setFilename,
    resetToDefaults,
  };
}
