import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

// Use the Inter font
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Markup to PDF Converter",
  description: "Convert Markdown to beautifully styled PDF documents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
