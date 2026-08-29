'use client';

import React, { useState } from 'react';
import { FileSpreadsheet, FileText, Loader2 } from 'lucide-react';

interface ExportButtonProps {
  reportId: string;
}

export default function ExportButton({ reportId }: ExportButtonProps) {
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);

  const handleDownload = async (format: 'pdf' | 'excel') => {
    try {
      setDownloadingFormat(format);
      const res = await fetch(`/api/report/export/${reportId || 'latest'}?format=${format}`);
      
      if (!res.ok) {
        throw new Error(`Failed to generate ${format.toUpperCase()} report.`);
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `GeM_Technical_Evaluation_${reportId.slice(0, 8)}.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error(err);
      alert(err.message || "Export download failed.");
    } finally {
      setDownloadingFormat(null);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-3">
      <button
        type="button"
        onClick={() => handleDownload('pdf')}
        disabled={downloadingFormat !== null}
        className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-300 transition-all flex items-center gap-2 shadow-sm"
      >
        {downloadingFormat === 'pdf' ? (
          <Loader2 className="w-3.5 h-3.5 animate-spin text-rose-700" />
        ) : (
          <FileText className="w-3.5 h-3.5 text-rose-700" />
        )}
        <span>Export Official PDF Report</span>
      </button>

      <button
        type="button"
        onClick={() => handleDownload('excel')}
        disabled={downloadingFormat !== null}
        className="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 transition-all flex items-center gap-2 shadow-sm"
      >
        {downloadingFormat === 'excel' ? (
          <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-700" />
        ) : (
          <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-700" />
        )}
        <span>Export Excel Matrix</span>
      </button>
    </div>
  );
}
