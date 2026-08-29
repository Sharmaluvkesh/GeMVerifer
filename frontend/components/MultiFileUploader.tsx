'use client';

import React, { useState } from 'react';
import { Upload, FileText, Trash2, ArrowRight, Loader2, Sparkles, FolderPlus, AlertTriangle } from 'lucide-react';
import { AnalysisReportResponse } from '../types';

interface MultiFileUploaderProps {
  onAnalysisComplete: (report: AnalysisReportResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  onLoadDemoData: () => void;
}

export default function MultiFileUploader({
  onAnalysisComplete,
  isLoading,
  setIsLoading,
  onLoadDemoData
}: MultiFileUploaderProps) {
  const [tenderFile, setTenderFile] = useState<File | null>(null);
  const [bidFiles, setBidFiles] = useState<File[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const handleTenderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setTenderFile(e.target.files[0]);
      setErrorMessage(null);
    }
  };

  const handleBidsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selected = Array.from(e.target.files);
      setBidFiles((prev) => [...prev, ...selected]);
      setErrorMessage(null);
    }
  };

  const removeBidFile = (index: number) => {
    setBidFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleRunAnalysis = async () => {
    if (!tenderFile) {
      setErrorMessage("Please select a GeM Tender PDF file first.");
      return;
    }
    if (bidFiles.length === 0) {
      setErrorMessage("Please select at least one Vendor Bid PDF file.");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      setUploadStatus("Extracting GeM Tender PDF specifications...");
      const tenderFormData = new FormData();
      tenderFormData.append("file", tenderFile);

      const tenderRes = await fetch("/api/upload-tender", {
        method: "POST",
        body: tenderFormData,
      });

      if (!tenderRes.ok) {
        const errData = await tenderRes.json();
        throw new Error(errData.detail || "Failed to upload tender PDF.");
      }

      const tenderData = await tenderRes.json();
      const tenderDbId = tenderData.tender_db_id;

      const bidDbIds: string[] = [];
      for (let i = 0; i < bidFiles.length; i++) {
        const file = bidFiles[i];
        setUploadStatus(`Extracting Vendor Bid ${i + 1} of ${bidFiles.length} (${file.name})...`);

        const bidFormData = new FormData();
        bidFormData.append("file", file);
        bidFormData.append("tender_db_id", tenderDbId);
        bidFormData.append("vendor_name_hint", file.name.replace(/\.[^/.]+$/, ""));

        const bidRes = await fetch("/api/upload-bid", {
          method: "POST",
          body: bidFormData,
        });

        if (!bidRes.ok) {
          const errData = await bidRes.json();
          throw new Error(errData.detail || `Failed to upload bid file ${file.name}`);
        }

        const bidData = await bidRes.json();
        bidDbIds.push(bidData.bid_db_id);
      }

      setUploadStatus("Running multi-parameter compliance matching & scoring...");
      const analyzeRes = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tender_db_id: tenderDbId,
          bid_db_ids: bidDbIds,
        }),
      });

      if (!analyzeRes.ok) {
        const errData = await analyzeRes.json();
        throw new Error(errData.detail || "Analysis calculation failed.");
      }

      const report: AnalysisReportResponse = await analyzeRes.json();
      onAnalysisComplete(report);
    } catch (err: any) {
      console.error(err);
      setErrorMessage(err.message || "An unexpected error occurred during processing.");
    } finally {
      setIsLoading(false);
      setUploadStatus('');
    }
  };

  return (
    <div id="uploader" className="gov-panel p-6 md:p-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2 font-display">
            <Upload className="w-5 h-5 text-blue-700" />
            Upload GeM Tender Notice & Vendor Submissions
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Drag & drop official PDF files to extract technical parameters, eligibility criteria, & vendor offered specs.
          </p>
        </div>
        
        <button
          onClick={onLoadDemoData}
          type="button"
          className="self-start md:self-auto px-4 py-2 text-xs font-semibold rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition-all flex items-center gap-1.5 shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-amber-700" />
          <span>Load Demo Sample Evaluation Data</span>
        </button>
      </div>

      {errorMessage && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-start gap-3 text-rose-800 text-xs">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <p>{errorMessage}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Tender Upload Box */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
            1. GeM Tender Notice Document (PDF) <span className="text-rose-600">*</span>
          </label>
          
          <div className={`border-2 border-dashed rounded-xl p-6 text-center transition-all ${
            tenderFile ? 'border-blue-400 bg-blue-50/40' : 'border-slate-300 hover:border-blue-500 bg-slate-50'
          }`}>
            <input
              type="file"
              accept=".pdf"
              id="tender-input"
              className="hidden"
              onChange={handleTenderChange}
            />
            {tenderFile ? (
              <div className="flex items-center justify-between bg-white p-3 rounded-lg border border-blue-200 shadow-sm">
                <div className="flex items-center space-x-3 truncate">
                  <FileText className="w-6 h-6 text-blue-700 shrink-0" />
                  <div className="truncate text-left">
                    <p className="text-xs font-medium text-slate-900 truncate">{tenderFile.name}</p>
                    <p className="text-[10px] text-slate-500">{(tenderFile.size / 1024).toFixed(1)} KB</p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setTenderFile(null)}
                  className="p-1 text-slate-400 hover:text-rose-600 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <label htmlFor="tender-input" className="cursor-pointer space-y-2 block">
                <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center mx-auto">
                  <FileText className="w-5 h-5" />
                </div>
                <div className="text-xs text-slate-700">
                  <span className="text-blue-700 font-semibold hover:underline">Click to upload PDF</span> or drag & drop file
                </div>
                <p className="text-[10px] text-slate-500">Extracts specs, tolerances, & eligibility criteria</p>
              </label>
            )}
          </div>
        </div>

        {/* Vendor Bids Upload Box */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider">
            2. Vendor Technical Bid Documents (PDFs) <span className="text-rose-600">*</span>
          </label>
          
          <div className="border-2 border-dashed border-slate-300 hover:border-emerald-500 bg-slate-50 rounded-xl p-6 text-center transition-all">
            <input
              type="file"
              accept=".pdf"
              multiple
              id="bids-input"
              className="hidden"
              onChange={handleBidsChange}
            />
            <label htmlFor="bids-input" className="cursor-pointer space-y-2 block">
              <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto">
                <FolderPlus className="w-5 h-5" />
              </div>
              <div className="text-xs text-slate-700">
                <span className="text-emerald-700 font-semibold hover:underline">Add Vendor PDF Bids</span> (Multiple supported)
              </div>
              <p className="text-[10px] text-slate-500">Upload seller catalogs, technical bids, & certificates</p>
            </label>
          </div>

          {/* Bid Files list */}
          {bidFiles.length > 0 && (
            <div className="space-y-2 max-h-40 overflow-y-auto pr-1">
              {bidFiles.map((file, idx) => (
                <div key={idx} className="flex items-center justify-between bg-white p-2.5 rounded-lg border border-slate-200 text-xs shadow-sm">
                  <div className="flex items-center space-x-2 truncate">
                    <FileText className="w-4 h-4 text-emerald-700 shrink-0" />
                    <span className="text-slate-800 font-medium truncate">{file.name}</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeBidFile(idx)}
                    className="p-1 text-slate-400 hover:text-rose-600 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Process Button */}
      <div className="pt-3 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs text-slate-600">
          {uploadStatus ? (
            <span className="flex items-center gap-2 text-blue-800 font-semibold animate-pulse">
              <Loader2 className="w-4 h-4 animate-spin text-blue-700" />
              {uploadStatus}
            </span>
          ) : (
            <span>Ready to evaluate {bidFiles.length} vendor bid(s) against tender.</span>
          )}
        </div>

        <button
          onClick={handleRunAnalysis}
          disabled={isLoading || !tenderFile || bidFiles.length === 0}
          type="button"
          className={`w-full sm:w-auto px-6 py-3 rounded-xl font-bold text-xs transition-all flex items-center justify-center space-x-2 shadow-md ${
            isLoading || !tenderFile || bidFiles.length === 0
              ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300'
              : 'bg-blue-800 hover:bg-blue-900 text-white shadow-blue-800/20'
          }`}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Evaluating Technical Bids...</span>
            </>
          ) : (
            <>
              <span>Run Technical Evaluation</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
