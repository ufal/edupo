import type { Metadata } from "next";
import metadata from "@/data/metadata.json";
import "./globals.css";

import { inter } from "./fonts";

import Header from "@/components/layout/Header";
import Main from "@/components/layout/Main";

export const pageMetadata: Metadata = metadata;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} font-light w-full flex flex-col min-h-screen bg-repeat antialiased`} style={{ backgroundImage: `url(${process.env.NEXT_PUBLIC_LINK_BASE || "/"}svg/uk-pattern-patterned.svg)` }}>
        <Header />
        <Main cls="flex-1 grid">
          { children }
        </Main>
      </body>
    </html>
  );
}
