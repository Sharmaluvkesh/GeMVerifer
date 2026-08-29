'use client';

import React from 'react';
import { ShieldCheck, Sparkles, Cpu, Building2, CheckCircle2 } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
      {/* Top Official Government Strip */}
      <div className="bg-[#0F2942] text-slate-200 px-6 py-1.5 text-xs font-medium flex items-center justify-between border-b border-slate-700">
        <div className="flex items-center space-x-3">
          <span className="flex items-center gap-1 text-slate-300 font-semibold">
            <Building2 className="w-3.5 h-3.5 text-amber-400" />
            Government e-Marketplace (GeM)
          </span>
          <span className="hidden sm:inline text-slate-500">•</span>
          <span className="hidden sm:inline text-slate-300">Ministry of Commerce and Industry</span>
        </div>
        <div className="flex items-center space-x-3 text-[11px]">
          <span className="bg-amber-500/20 text-amber-300 font-bold px-2 py-0.5 rounded border border-amber-500/30">
            SIH Problem Statement
          </span>
          <span className="hidden md:inline text-emerald-400 flex items-center gap-1 font-semibold">
            <CheckCircle2 className="w-3 h-3" /> Official Evaluation Portal
          </span>
        </div>
      </div>

      {/* Tricolor Accent Strip */}
      <div className="gov-tricolor-line" />

      {/* Main Navbar */}
      <div className="max-w-7xl mx-auto px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-3.5">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-950 text-white flex items-center justify-center shadow-md shadow-blue-900/10 border border-blue-700/30">
            <ShieldCheck className="w-6 h-6 text-amber-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-slate-900 font-display">
                GeM <span className="text-blue-700">Bid Analyzer</span>
              </h1>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-800 border border-blue-200">
                v1.0 Official
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium">Government e-Marketplace Automated Technical Evaluation Engine</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center space-x-2 text-xs text-slate-600 bg-slate-100 px-3.5 py-1.5 rounded-lg border border-slate-200">
            <Cpu className="w-3.5 h-3.5 text-blue-700" />
            <span>AI Parser: <strong className="text-slate-800">pdfplumber + Gemini 2.5</strong></span>
          </div>
          <a
            href="#uploader"
            className="flex items-center space-x-2 text-xs font-semibold px-4 py-2 rounded-lg bg-blue-700 hover:bg-blue-800 text-white transition-all shadow-md shadow-blue-700/20"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>New Tender Evaluation</span>
          </a>
        </div>
      </div>
    </header>
  );
}
