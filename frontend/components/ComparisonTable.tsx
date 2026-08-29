'use client';

import React, { useState } from 'react';
import { Search, Filter, CheckCircle2, XCircle, AlertTriangle, Info, HelpCircle } from 'lucide-react';
import { TenderSpecification, VendorEvaluationResult, ParameterComparisonResult } from '../types';

interface ComparisonTableProps {
  tenderInfo: TenderSpecification;
  vendors: VendorEvaluationResult[];
}

export default function ComparisonTable({ tenderInfo, vendors }: ComparisonTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'COMPLIANT' | 'NON_COMPLIANT' | 'NEEDS_REVIEW'>('ALL');
  const [selectedExplanation, setSelectedExplanation] = useState<{ paramName: string; vendorName: string; res: ParameterComparisonResult } | null>(null);

  if (!tenderInfo || !vendors || vendors.length === 0) return null;

  const parameters = tenderInfo.technical_parameters || [];

  const filteredParameters = parameters.filter((param) => {
    const matchesSearch = param.parameter_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          param.required_value.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return false;
    if (statusFilter === 'ALL') return true;

    return vendors.some((v) => {
      const res = v.parameter_results.find((r) => r.parameter_name === param.parameter_name);
      return res?.status === statusFilter;
    });
  });

  const getStatusBadge = (res?: ParameterComparisonResult) => {
    if (!res) {
      return (
        <span className="inline-flex items-center gap-1 text-[11px] px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-500 border border-slate-200">
          <HelpCircle className="w-3 h-3" /> N/A
        </span>
      );
    }

    switch (res.status) {
      case 'COMPLIANT':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-300">
            <CheckCircle2 className="w-3 h-3 text-emerald-700 shrink-0" />
            COMPLIANT
          </span>
        );
      case 'NON_COMPLIANT':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-800 border border-rose-300">
            <XCircle className="w-3 h-3 text-rose-700 shrink-0" />
            NON-COMPLIANT
          </span>
        );
      case 'NEEDS_REVIEW':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-900 border border-amber-300">
            <AlertTriangle className="w-3 h-3 text-amber-700 shrink-0" />
            NEEDS REVIEW
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="gov-panel p-6 space-y-5">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h2 className="text-xl font-bold text-slate-900 font-display flex items-center gap-2">
            <Filter className="w-5 h-5 text-blue-700" />
            Side-by-Side Technical Evaluation Matrix
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Compare vendor offered specifications directly against GeM tender requirements with color-coded compliance status.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search Box */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search parameter..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-700 focus:bg-white transition-colors w-48 shadow-sm"
            />
          </div>

          {/* Status Tabs */}
          <div className="flex items-center bg-slate-100 rounded-xl p-1 border border-slate-200">
            {(['ALL', 'COMPLIANT', 'NON_COMPLIANT', 'NEEDS_REVIEW'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setStatusFilter(tab)}
                className={`px-3 py-1 text-[11px] font-semibold rounded-lg transition-all ${
                  statusFilter === tab
                    ? 'bg-blue-800 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {tab === 'ALL' ? 'All' : tab.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Rationale Modal / Dialog Box if clicked */}
      {selectedExplanation && (
        <div className="bg-blue-50/80 border border-blue-200 rounded-xl p-4 flex items-start justify-between gap-4 animate-fadeIn shadow-sm">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-700 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1 text-slate-800">
              <p className="font-bold text-slate-900">
                Discrepancy Rationale: <span className="text-blue-800">{selectedExplanation.paramName}</span> ({selectedExplanation.vendorName})
              </p>
              <p className="text-slate-700">{selectedExplanation.res.explanation}</p>
              <div className="flex items-center gap-4 text-[11px] text-slate-600 pt-1">
                <span>Tender Req: <strong className="text-slate-900">{selectedExplanation.res.tender_required_value}</strong></span>
                <span>Vendor Offered: <strong className="text-slate-900">{selectedExplanation.res.vendor_offered_value}</strong></span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setSelectedExplanation(null)}
            className="text-slate-500 hover:text-slate-900 text-xs font-bold px-2 py-1 bg-blue-100 rounded border border-blue-200"
          >
            ✕
          </button>
        </div>
      )}

      {/* Side-by-Side Matrix Table */}
      <div className="overflow-x-auto rounded-xl border border-slate-300 shadow-sm">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-100 text-slate-800 font-bold border-b border-slate-300">
              <th className="p-3.5 min-w-[180px]">Parameter Name</th>
              <th className="p-3.5 min-w-[200px] bg-slate-200/50 border-x border-slate-300">Tender Requirement</th>
              {vendors.map((vendor, idx) => (
                <th key={idx} className="p-3.5 min-w-[220px]">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 truncate">{vendor.vendor_name}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                      vendor.is_disqualified ? 'bg-rose-100 text-rose-800 border-rose-300' : 'bg-emerald-100 text-emerald-800 border-emerald-300'
                    }`}>
                      {vendor.technical_score}%
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white">
            {filteredParameters.length === 0 ? (
              <tr>
                <td colSpan={2 + vendors.length} className="p-8 text-center text-slate-500 text-xs">
                  No technical parameters found matching the current search/filter criteria.
                </td>
              </tr>
            ) : (
              filteredParameters.map((param, pIdx) => (
                <tr key={pIdx} className="hover:bg-slate-50 transition-colors">
                  {/* Parameter Name */}
                  <td className="p-3.5 font-semibold text-slate-900">
                    <div className="space-y-1">
                      <div className="flex items-center gap-1.5">
                        <span>{param.parameter_name}</span>
                        {param.mandatory && (
                          <span className="text-[9px] uppercase font-bold text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">
                            Mandatory
                          </span>
                        )}
                      </div>
                      {param.tolerance && (
                        <p className="text-[10px] text-slate-500 font-normal">Tol: {param.tolerance}</p>
                      )}
                    </div>
                  </td>

                  {/* Required Value */}
                  <td className="p-3.5 text-slate-800 font-mono bg-slate-50/80 border-x border-slate-200 font-medium">
                    {param.required_value}
                  </td>

                  {/* Vendor Offered Values & Status Badges */}
                  {vendors.map((vendor, vIdx) => {
                    const res = vendor.parameter_results.find((r) => r.parameter_name === param.parameter_name);

                    return (
                      <td key={vIdx} className="p-3.5">
                        <div className="space-y-1.5">
                          <div className="flex items-center justify-between gap-2">
                            {getStatusBadge(res)}
                            {res?.explanation && (
                              <button
                                type="button"
                                title="Click to view explanation"
                                onClick={() => setSelectedExplanation({ paramName: param.parameter_name, vendorName: vendor.vendor_name, res })}
                                className="text-slate-400 hover:text-blue-700 p-0.5 transition-colors"
                              >
                                <Info className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                          <p className="text-slate-800 font-mono text-[11px] font-medium truncate" title={res?.vendor_offered_value}>
                            {res?.vendor_offered_value || 'NOT PROVIDED'}
                          </p>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
