'use client';

import React from 'react';
import { Award, FileX, CheckCircle, ShieldAlert, TrendingUp } from 'lucide-react';
import { VendorEvaluationResult } from '../types';

interface SummaryCardProps {
  vendors: VendorEvaluationResult[];
  itemName: string;
}

export default function SummaryCard({ vendors, itemName }: SummaryCardProps) {
  if (!vendors || vendors.length === 0) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-slate-900 font-display flex items-center gap-2">
          <Award className="w-5 h-5 text-blue-700" />
          Technical Compliance Summary Matrix
        </h2>
        <span className="text-xs text-slate-500 font-medium">
          Tender Item: <strong className="text-slate-800">{itemName}</strong>
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {vendors.map((vendor, idx) => {
          const isDisq = vendor.is_disqualified;
          const score = vendor.technical_score;

          // Color themes for official government light mode
          const badgeBg = isDisq
            ? 'bg-rose-50 border-rose-200 text-rose-800 font-bold'
            : score >= 80
            ? 'bg-emerald-50 border-emerald-200 text-emerald-800 font-bold'
            : 'bg-amber-50 border-amber-200 text-amber-800 font-bold';

          const scoreColor = isDisq
            ? 'text-rose-700'
            : score >= 80
            ? 'text-emerald-700'
            : 'text-amber-700';

          const progressBg = isDisq
            ? 'bg-rose-600'
            : score >= 80
            ? 'bg-emerald-600'
            : 'bg-amber-600';

          return (
            <div
              key={idx}
              className="gov-card p-5 relative overflow-hidden border border-slate-200 hover:border-slate-300 transition-all flex flex-col justify-between"
            >
              {/* Top Accent Line */}
              <div className={`absolute top-0 left-0 right-0 h-1.5 ${progressBg}`} />

              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <h3 className="font-bold text-slate-900 text-base font-display truncate max-w-[180px]" title={vendor.vendor_name}>
                      {vendor.vendor_name}
                    </h3>
                    <p className="text-[11px] text-slate-500">Bid Ref: {vendor.bid_id || 'N/A'}</p>
                  </div>
                  
                  <span className={`text-[10px] uppercase tracking-wider px-2.5 py-1 rounded-md border ${badgeBg}`}>
                    {isDisq ? 'Disqualified' : 'Qualified'}
                  </span>
                </div>

                {/* Score Gauge Block */}
                <div className="bg-slate-50 rounded-xl p-4 my-3 border border-slate-200">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-xs font-semibold text-slate-600 flex items-center gap-1">
                      <TrendingUp className="w-3.5 h-3.5 text-blue-700" />
                      Technical Compliance Score
                    </span>
                    <span className={`text-2xl font-extrabold ${scoreColor} font-display`}>
                      {score}%
                    </span>
                  </div>

                  <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all duration-700 ${progressBg}`}
                      style={{ width: `${Math.min(score, 100)}%` }}
                    />
                  </div>
                </div>

                {/* Disqualification Rationale */}
                {isDisq && vendor.disqualification_reasons.length > 0 && (
                  <div className="bg-rose-50 border border-rose-200 rounded-xl p-3 mb-3 text-xs space-y-1.5">
                    <div className="flex items-center gap-1.5 text-rose-800 font-bold text-[11px]">
                      <ShieldAlert className="w-3.5 h-3.5 shrink-0 text-rose-600" />
                      Disqualification Rationale:
                    </div>
                    <ul className="list-disc list-inside space-y-1 text-rose-900 text-[11px] pl-1">
                      {vendor.disqualification_reasons.map((reason, rIdx) => (
                        <li key={rIdx} className="leading-tight">{reason}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Missing Documents Alert */}
                {vendor.missing_documents.length > 0 && (
                  <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 text-xs space-y-1 text-amber-900">
                    <div className="flex items-center gap-1.5 font-bold text-[11px] text-amber-800">
                      <FileX className="w-3.5 h-3.5 shrink-0 text-amber-600" />
                      Missing Eligibility Certificates:
                    </div>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {vendor.missing_documents.map((doc, dIdx) => (
                        <span key={dIdx} className="bg-amber-100/80 border border-amber-300 text-amber-950 text-[10px] px-2 py-0.5 rounded font-medium">
                          {doc}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-medium">
                <span>Evaluated Specs: {vendor.parameter_results.length}</span>
                <span className="flex items-center gap-1 text-emerald-700 font-semibold">
                  <CheckCircle className="w-3 h-3 text-emerald-600" />
                  {vendor.parameter_results.filter(p => p.status === 'COMPLIANT').length} Compliant
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
