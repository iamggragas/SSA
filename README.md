# 🚀 SSA Forecasting Tool
A modern, web-based application utilizing Singular Spectrum Analysis (SSA) to forecast both future revenue and specific inventory data based on historical trends. The process is simple: select your tool mode, upload your data, configure your parameters, and predict!

## 🛠 Tech Stack
- **Frontend:** React.js, Vite, React Router (Modern & Responsive UI)
- **Backend:** FastAPI (High-performance Python framework)
- **Algorithm:** Singular Spectrum Analysis (SSA) via powerful scientific packages

## 📋 Data Upload Requirements
To ensure accurate forecasting, please ensure your CSV or Excel file conforms to the structural prerequisites of the tool you intend to use. Note that empty rows will be automatically dropped.

### Revenue Forecaster
Demands a strict 2-column configuration:
| Column Name | Description | Format |
| :--- | :--- | :--- |
| **Date** | The timeline of the data | YYYY-MM-DD (e.g., 2026-04-05) |
| **Value** | The revenue or target metric to forecast | Numeric (e.g., 150.50) |

### Inventory Forecaster
Supports flexible multi-column uploads to forecast individual units:
| Column Index | Field | Description |
| :--- | :--- | :--- |
| **Column 1** | **Date** | The timeline of the data |
| **Column 2..N** | **Products** | Various numeric inventory values for corresponding distinct tracking metrics |

## 💡 How to Use
1. **Navigate:** Choose either the *Revenue Forecaster* or *Inventory Forecaster* via the sidebar navigation.
2. **Upload:** Drag and drop your `.csv` or `.xlsx` data file.
3. **Configure:** Select a specific Product Data Column (if using Inventory mode), pick the interval format (daily, weekly, monthly, strictly specific days), and enter the desired duration.
4. **Analyze:** Click the predict button and let the Python FastAPI backend churn via SSA logic.
5. **Result:** Visualize the generated historical+forecasted graphical layout and exact parsed tables.

## ⚙️ Installation & Setup

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
