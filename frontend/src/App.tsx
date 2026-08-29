import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import MultiFileUploader from '../components/MultiFileUploader';
import SummaryCard from '../components/SummaryCard';
import ComparisonTable from '../components/ComparisonTable';
import ExportButton from '../components/ExportButton';
import { AnalysisReportResponse } from '../types';
import { BarChart3, Building2 } from 'lucide-react';

const DEMO_REPORT_DATA: AnalysisReportResponse = {
  report_id: "GEM-EVAL-2026-001",
  evaluated_at: new Date().toISOString(),
  tender_info: {
    tender_id: "GEM/2026/B/8941205",
    item_name: "High-Performance Workstation Laptops (GeM Custom Bid)",
    publishing_date: "2026-08-15",
    eligibility_criteria: [
      "Minimum Annual Turnover of INR 50 Lakhs in last 3 financial years",
      "Valid ISO 9001:2015 Certification",
      "At least 3 years of past experience in Government procurement",
      "GST Registration Certificate"
    ],
    technical_parameters: [
      {
        parameter_name: "Processor / CPU",
        required_value: "Intel Core i7 13th Gen (16 Cores, 24 Threads) or AMD Ryzen 7 7840HS",
        tolerance: "Min 14 Cores",
        mandatory: true,
        weight: 2.0
      },
      {
        parameter_name: "RAM / Memory",
        required_value: "32 GB DDR5 5600MHz",
        tolerance: "Min 32 GB",
        mandatory: true,
        weight: 1.5
      },
      {
        parameter_name: "Storage Capacity",
        required_value: "1 TB NVMe M.2 PCIe 4.0 SSD",
        tolerance: "Min 1 TB",
        mandatory: true,
        weight: 1.5
      },
      {
        parameter_name: "Graphics Card (GPU)",
        required_value: "NVIDIA RTX 4060 8GB GDDR6 Dedicated VRAM",
        tolerance: "Min 6GB VRAM",
        mandatory: false,
        weight: 1.0
      },
      {
        parameter_name: "Display Screen",
        required_value: "16 Inch WQXGA (2560x1600) 165Hz IPS 100% sRGB",
        tolerance: "+/- 0.4 inch",
        mandatory: false,
        weight: 1.0
      },
      {
        parameter_name: "Warranty & Support",
        required_value: "3 Years Onsite Comprehensive OEM Warranty",
        tolerance: "Min 3 Years",
        mandatory: true,
        weight: 1.5
      }
    ]
  },
  vendors: [
    {
      vendor_name: "TechNova Solutions Ltd",
      bid_id: "BID-GEM-9901",
      technical_score: 100.0,
      is_disqualified: false,
      disqualification_reasons: [],
      missing_documents: [],
      parameter_results: [
        {
          parameter_name: "Processor / CPU",
          tender_required_value: "Intel Core i7 13th Gen (16 Cores, 24 Threads) or AMD Ryzen 7 7840HS",
          vendor_offered_value: "Intel Core i7-13700H (14 Cores / 20 Threads, 5.0 GHz)",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Offered specification satisfies minimum core threshold requirement (14 Cores)."
        },
        {
          parameter_name: "RAM / Memory",
          tender_required_value: "32 GB DDR5 5600MHz",
          vendor_offered_value: "32 GB DDR5 5600MHz (2x16GB SODIMM)",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Exact match with tender requirement."
        },
        {
          parameter_name: "Storage Capacity",
          tender_required_value: "1 TB NVMe M.2 PCIe 4.0 SSD",
          vendor_offered_value: "1 TB NVMe M.2 Gen4 SSD (Up to 7000MB/s)",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Offered numeric value (1 TB) meets minimum requirement."
        },
        {
          parameter_name: "Graphics Card (GPU)",
          tender_required_value: "NVIDIA RTX 4060 8GB GDDR6 Dedicated VRAM",
          vendor_offered_value: "NVIDIA GeForce RTX 4060 8GB GDDR6",
          status: "COMPLIANT",
          is_mandatory: false,
          score: 1.0,
          explanation: "Exact match with tender requirements."
        },
        {
          parameter_name: "Display Screen",
          tender_required_value: "16 Inch WQXGA (2560x1600) 165Hz IPS 100% sRGB",
          vendor_offered_value: "16.0 Inch QHD+ (2560x1600) 165Hz IPS",
          status: "COMPLIANT",
          is_mandatory: false,
          score: 1.0,
          explanation: "High semantic equivalence (95%) with tender requirement."
        },
        {
          parameter_name: "Warranty & Support",
          tender_required_value: "3 Years Onsite Comprehensive OEM Warranty",
          vendor_offered_value: "3 Years Onsite OEM Warranty + ADP",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Meets 3 Years Onsite requirement."
        }
      ]
    },
    {
      vendor_name: "Apex Micro Systems",
      bid_id: "BID-GEM-8812",
      technical_score: 64.7,
      is_disqualified: true,
      disqualification_reasons: [
        "Failed mandatory technical parameter 'Processor / CPU': Offered numeric value (Intel i5-12400) is below minimum requirement."
      ],
      missing_documents: ["ISO Quality Certificate", "Financial Turnover Certificate / Audited Statements"],
      parameter_results: [
        {
          parameter_name: "Processor / CPU",
          tender_required_value: "Intel Core i7 13th Gen (16 Cores, 24 Threads) or AMD Ryzen 7 7840HS",
          vendor_offered_value: "Intel Core i5-12400 (6 Cores / 12 Threads)",
          status: "NON_COMPLIANT",
          is_mandatory: true,
          score: 0.0,
          explanation: "Offered specification (Intel i5 6 Cores) is below minimum required 14 Cores."
        },
        {
          parameter_name: "RAM / Memory",
          tender_required_value: "32 GB DDR5 5600MHz",
          vendor_offered_value: "16 GB DDR4 3200MHz",
          status: "NON_COMPLIANT",
          is_mandatory: true,
          score: 0.0,
          explanation: "Offered value (16 GB) is below minimum requirement (32 GB) by 16.0 GB."
        },
        {
          parameter_name: "Storage Capacity",
          tender_required_value: "1 TB NVMe M.2 PCIe 4.0 SSD",
          vendor_offered_value: "1 TB NVMe M.2 SSD",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Offered numeric value (1 TB) meets minimum requirement."
        },
        {
          parameter_name: "Graphics Card (GPU)",
          tender_required_value: "NVIDIA RTX 4060 8GB GDDR6 Dedicated VRAM",
          vendor_offered_value: "NVIDIA RTX 3050 4GB GDDR6",
          status: "NON_COMPLIANT",
          is_mandatory: false,
          score: 0.0,
          explanation: "Offered VRAM (4GB) is inferior to required 8GB VRAM."
        },
        {
          parameter_name: "Display Screen",
          tender_required_value: "16 Inch WQXGA (2560x1600) 165Hz IPS 100% sRGB",
          vendor_offered_value: "15.6 Inch Full HD (1920x1080) 60Hz",
          status: "NEEDS_REVIEW",
          is_mandatory: false,
          score: 0.5,
          explanation: "Partial match. Offered 15.6 inch screen within +/- 0.4 inch tolerance, but resolution is FHD."
        },
        {
          parameter_name: "Warranty & Support",
          tender_required_value: "3 Years Onsite Comprehensive OEM Warranty",
          vendor_offered_value: "3 Years Onsite Comprehensive Warranty",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Exact match with tender requirements."
        }
      ]
    },
    {
      vendor_name: "Paramount Enterprises",
      bid_id: "BID-GEM-7740",
      technical_score: 94.1,
      is_disqualified: false,
      disqualification_reasons: [],
      missing_documents: [],
      parameter_results: [
        {
          parameter_name: "Processor / CPU",
          tender_required_value: "Intel Core i7 13th Gen (16 Cores, 24 Threads) or AMD Ryzen 7 7840HS",
          vendor_offered_value: "AMD Ryzen 7 7840HS (8 Cores / 16 Threads, 5.1 GHz)",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Exact match with tender specified CPU model."
        },
        {
          parameter_name: "RAM / Memory",
          tender_required_value: "32 GB DDR5 5600MHz",
          vendor_offered_value: "64 GB DDR5 5600MHz",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Offered specification (64 GB) exceeds minimum requirement (32 GB)."
        },
        {
          parameter_name: "Storage Capacity",
          tender_required_value: "1 TB NVMe M.2 PCIe 4.0 SSD",
          vendor_offered_value: "2 TB NVMe M.2 Gen4 SSD",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Offered numeric value (2 TB) exceeds minimum requirement (1 TB)."
        },
        {
          parameter_name: "Graphics Card (GPU)",
          tender_required_value: "NVIDIA RTX 4060 8GB GDDR6 Dedicated VRAM",
          vendor_offered_value: "NVIDIA RTX 4060 8GB GDDR6",
          status: "COMPLIANT",
          is_mandatory: false,
          score: 1.0,
          explanation: "Exact match with tender requirement."
        },
        {
          parameter_name: "Display Screen",
          tender_required_value: "16 Inch WQXGA (2560x1600) 165Hz IPS 100% sRGB",
          vendor_offered_value: "15.6 Inch QHD (2560x1440) OLED",
          status: "NEEDS_REVIEW",
          is_mandatory: false,
          score: 0.5,
          explanation: "Partial match. Offered OLED screen has higher contrast but 16:9 ratio instead of 16:10."
        },
        {
          parameter_name: "Warranty & Support",
          tender_required_value: "3 Years Onsite Comprehensive OEM Warranty",
          vendor_offered_value: "3 Years Onsite Warranty",
          status: "COMPLIANT",
          is_mandatory: true,
          score: 1.0,
          explanation: "Satisfies minimum 3 year onsite requirement."
        }
      ]
    }
  ]
};

export default function App() {
  const [report, setReport] = useState<AnalysisReportResponse | null>(DEMO_REPORT_DATA);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalysisComplete = (newReport: AnalysisReportResponse) => {
    setReport(newReport);
  };

  const handleLoadDemoData = () => {
    setReport(DEMO_REPORT_DATA);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 space-y-8">
        <div className="bg-white rounded-2xl p-8 relative overflow-hidden border border-slate-300 shadow-sm">
          <div className="max-w-3xl space-y-3">
            <div className="inline-flex items-center space-x-2 bg-blue-50 border border-blue-200 px-3.5 py-1 rounded-full text-xs font-bold text-blue-900">
              <Building2 className="w-3.5 h-3.5 text-amber-700" />
              <span>Government e-Marketplace Technical Bid Evaluation System</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900 font-display tracking-tight leading-tight">
              Automated Technical Compliance & <span className="text-blue-700">Bid Analyzer</span>
            </h1>
            <p className="text-sm text-slate-600 leading-relaxed font-normal">
              Parse messy PDF tender specifications and vendor bids using <strong className="text-slate-900">pdfplumber</strong> and <strong className="text-slate-900">Google Gemini API</strong>. Compare offered specs against requirements using exact numeric tolerance checks, fuzzy matching, and weighted technical compliance scoring.
            </p>
          </div>
        </div>

        <MultiFileUploader
          onAnalysisComplete={handleAnalysisComplete}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
          onLoadDemoData={handleLoadDemoData}
        />

        {report && (
          <div className="space-y-8 animate-fadeIn">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
              <div>
                <h2 className="text-2xl font-bold text-slate-900 font-display flex items-center gap-2">
                  <BarChart3 className="w-6 h-6 text-blue-700" />
                  Technical Evaluation Dashboard
                </h2>
                <p className="text-xs text-slate-500 mt-1 font-medium">
                  Report Reference: <span className="font-mono text-slate-800 font-bold">{report.report_id}</span> | Evaluated Date: {report.evaluated_at ? new Date(report.evaluated_at).toLocaleDateString() : 'Today'}
                </p>
              </div>

              <ExportButton reportId={report.report_id} />
            </div>

            <SummaryCard
              vendors={report.vendors}
              itemName={report.tender_info.item_name}
            />

            <ComparisonTable
              tenderInfo={report.tender_info}
              vendors={report.vendors}
            />
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-600 mt-12 shadow-inner">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>© 2026 Government e-Marketplace (GeM) - Technical Evaluation Engine. All Rights Reserved.</p>
          <div className="flex items-center space-x-4 text-slate-500 font-medium">
            <span>FastAPI 0.110</span>
            <span>•</span>
            <span>Next.js App Router</span>
            <span>•</span>
            <span>Google Gemini 2.5 Flash</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
