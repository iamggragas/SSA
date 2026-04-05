# 🚀 SSA Forecasting Tool
A web-based application utilizing Singular Spectrum Analysis (SSA) to predict future prices based on historical data. Process is simple: upload, configure, and predict!

## 🛠 Tech Stack
- **Frontend:** React.js (Modern & Responsive UI)
- **Backend:** FastAPI (High-performance Python framework)
- **Algorithm:** Singular Spectrum Analysis (SSA)

## 📋 Data Upload Requirements
To ensure accurate forecasting, please make sure your CSV file contains exactly two columns:

| Column Name | Description | Format |
| :--- | :--- | :--- |
| **date** | The timeline of the data | YYYY-MM-DD (e.g., 2026-04-05) |
| **price** | The value you wish to forecast | Numeric (e.g., 150.50) |

*Note: Please ensure there are no empty rows in your CSV file to prevent computation errors.*

## 💡 How to Use
1. **Upload:** Upload your 2-column CSV file.
2. **Configure:** Input the number of days you want to predict into the future.
3. **Analyze:** Click the predict button and wait for the results from the FastAPI backend.
4. **Result:** View the generated graph and table of forecasted values.

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
npm start
```
