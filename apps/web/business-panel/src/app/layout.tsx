import type { Metadata } from "next";

import "./globals.css";


export const metadata: Metadata = {
  title: "Reservatior",
  description: "Panel rezerwacji dla firm",
};


export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pl">
      <body>{children}</body>
    </html>
  );
}
