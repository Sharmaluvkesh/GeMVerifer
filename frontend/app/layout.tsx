import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GeM Bid Analyzer - Automated Technical Bid Evaluation System',
  description: 'AI-powered Government e-Marketplace (GeM) Tender PDF and Vendor Bid PDF compliance scoring and side-by-side comparison matrix.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen bg-[#0b0f19] text-slate-100 selection:bg-blue-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
