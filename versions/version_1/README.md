# GeM Bid Analyzer 🛡️⚡

An AI-powered full-stack solution for automated technical bid evaluation, parameter matching, and compliance scoring of **Government e-Marketplace (GeM)** tender documents against vendor bid submissions (SIH Problem Statement).

---

## 🌟 Key Features

1. **Multi-File PDF Extractor (`extractor.py`)**:
   - Uses `pdfplumber` to extract raw text and tables from GeM Tender PDFs and Vendor Bid PDFs.
   - Leverages **Google Gemini API (`google-genai` SDK)** with structured JSON output schema (`TenderSpecification` and `VendorBid` Pydantic models).
   - Includes rule-based heuristic fallback for offline operation.

2. **Advanced Compliance & Comparison Engine (`comparator.py`)**:
   - **Exact Matching**: Checks verbatim string specs & units.
   - **Numeric Range & Tolerance Check**: Automatic unit normalization (`GB`/`TB`/`GHz`/`Lakhs`) and threshold check (`>= Min 16GB`).
   - **Semantic Text Matching**: Normalized similarity for descriptive specs with confidence scores.
   - **Weighted Scoring**: Technical score calculation (0–100%).
   - **Disqualification Logic**: Automatic flag & rationale when mandatory parameters fail.
   - **Eligibility Auditor**: Cross-checks mandatory certificates (ISO, Turnover, GST, Past Experience).

3. **Modern Next.js Dashboard**:
   - **Multi-File Drag & Drop Zone**: Upload GeM Tender Notice PDF + multiple Vendor Bids.
   - **Side-by-Side Comparison Matrix**: Interactive color-coded table (Green = COMPLIANT, Red = NON_COMPLIANT, Yellow = NEEDS_REVIEW).
   - **Summary Cards**: Overall score %, disqualification flags, and missing document alerts.
   - **Instant Search & Status Filters**: Easily filter parameters by status or search terms.
   - **PDF & Excel Exporter**: One-click download of PDF Technical Evaluation Reports and Excel evaluation matrix.

---

## 🏗️ Project Architecture

```
geM bid analyzer/
├── backend/
│   ├── app/
│   │   ├── config.py         # App configuration & settings
│   │   ├── database.py       # SQLAlchemy SQLite/Postgres DB setup
│   │   ├── models.py         # DB Models (Tender, Bid, Report)
│   │   ├── schemas.py        # Strict Pydantic models (TenderSpecification, VendorBid, etc.)
│   │   ├── extractor.py      # pdfplumber + Gemini LLM structured PDF parser
│   │   ├── comparator.py     # Parameter matcher, scoring engine & discrepancy rationale
│   │   ├── reporter.py       # ReportLab PDF & openpyxl Excel matrix generator
│   │   ├── routes/
│   │   │   ├── upload.py     # /api/upload-tender & /api/upload-bid
│   │   │   ├── analyze.py    # /api/analyze
│   │   │   └── report.py     # /api/report & /api/report/export
│   │   └── main.py           # FastAPI entrypoint & CORS config
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Main evaluation dashboard
│   │   ├── layout.tsx
│   │   └── globals.css       # Tailwind & Glassmorphism styles
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── MultiFileUploader.tsx
│   │   ├── SummaryCard.tsx
│   │   ├── ComparisonTable.tsx
│   │   └── ExportButton.tsx
│   ├── types/index.ts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── start.bat                 # One-click Windows launch script
├── start.sh                  # One-click Linux/macOS launch script
└── .env.example
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- (Optional) Google Gemini API Key

### Option 1: Using Start Script (Windows)
Double-click `start.bat` or run in terminal:
```cmd
start.bat
```

### Option 2: Using Start Script (Linux / macOS)
```bash
chmod +x start.sh
./start.sh
```

### Option 3: Manual Execution

1. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Linux/macOS: source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Open your browser at:
- **Frontend Dashboard**: `http://localhost:3000`
- **FastAPI API Docs**: `http://localhost:8000/docs`

---

## 🐳 Docker Deployment

To run both backend and frontend using Docker Compose:

```bash
docker-compose up --build
```

---

## 📡 API Reference Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload-tender` | Upload GeM Tender Notice PDF & extract specifications |
| `POST` | `/api/upload-bid` | Upload Vendor Bid PDF & extract submitted parameters |
| `POST` | `/api/analyze` | Run compliance comparison & generate technical score |
| `GET`  | `/api/report/{id}` | Retrieve evaluation JSON report by ID |
| `GET`  | `/api/report/export/{id}?format=pdf` | Export downloadable PDF Evaluation Report |
| `GET`  | `/api/report/export/{id}?format=excel` | Export downloadable Excel Evaluation Matrix |
