from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import io
import datetime
from ssa import SSA

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/forecast")
async def forecast(file: UploadFile = File(...), forecast_days: int = Form(...)):
    try:
        contents = await file.read()
        
        # Determine file type and read into pandas
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
            if len(df.columns) < 2:
                raise Exception("File must have at least two columns.")
            # Standardize columns
            df = df.iloc[:, :2]
            df.columns = ['Date', 'Value']
        elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            # The previous logic had header=None, names=['Date', 'Value'] but let's try to infer if columns are present 
            # Or we can just take the first two columns and rename them.
            try:
                df = pd.read_excel(io.BytesIO(contents))
                if len(df.columns) < 2:
                    raise Exception("File must have at least two columns.")
                # We'll just take the first two columns and assume they are Date and Value
                df = df.iloc[:, :2]
                df.columns = ['Date', 'Value']
            except:
                # Fallback to no header
                df = pd.read_excel(io.BytesIO(contents), header=None)
                df = df.iloc[:, :2]
                df.columns = ['Date', 'Value']
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV or Excel file.")

        # Convert date to datetime, handle errors
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        # Drop rows with invalid dates or missing values
        df = df.dropna(subset=['Date', 'Value'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        if len(df) < 10:
            raise HTTPException(status_code=400, detail="Not enough data points for SSA.")

        # Determine L based on data length. Default is 30, but cap at len(df) // 2
        L = 30
        if len(df) < 60:
            L = len(df) // 2

        # Initialize SSA
        ssa = SSA(df['Value'].values, L=L)

        # Extract components
        trend = ssa.reconstruct(0)
        seasonality = ssa.reconstruct([1, 2, 3])
        noise = df['Value'] - trend - seasonality
        
        # Forecast
        forecast_vals = ssa.forecast([0, 1, 2, 3], steps=forecast_days)
        
        # Generate future dates
        last_date = df['Date'].iloc[-1]
        
        # Try to infer frequency, fallback to 1 day
        try:
            freq = df['Date'].diff().median()
            if pd.isna(freq):
                freq = pd.Timedelta(days=1)
        except:
            freq = pd.Timedelta(days=1)
            
        forecast_dates = [last_date + freq * i for i in range(1, forecast_days + 1)]

        # Prepare response
        # We need to send back dates as strings
        # Also handle any NaN or infinite values
        df['Value'] = df['Value'].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        historical_data = {
            "dates": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            "values": df['Value'].tolist(),
            "trend": trend.tolist(),
            "seasonality": seasonality.tolist(),
            "noise": noise.tolist()
        }
        
        forecast_data = {
            "dates": [d.strftime('%Y-%m-%d') for d in forecast_dates],
            "values": forecast_vals.tolist()
        }

        return {
            "historical": historical_data,
            "forecast": forecast_data
        }

    except Exception as e:
        import traceback
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\nTraceback: {tb_str}")
