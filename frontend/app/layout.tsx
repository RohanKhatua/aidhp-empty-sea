import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from '@/components/theme-provider';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'GATE',
  description: 'GATE is a modular email processing pipeline designed to automate workflows using **n8n** and manage data persistence with **MongoDB**. It processes incoming emails, extracts relevant information, classifies them, and sends notifications to appropriate teams. This project aims to streamline email-based workflows for businesses.',
  generator: 'Next.js',
  
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
