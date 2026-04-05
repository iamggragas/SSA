import nbformat as nbf
import os

def build_notebook():
    nb = nbf.v4.new_notebook()

    cell_1 = nbf.v4.new_markdown_cell("# Monthly Singular Spectrum Analysis (SSA)\n\nThis notebook performs SSA on `mothly.xlsx` (3 years of data, N=36), extracts trend, seasonality, and noise respectively, and forecasts the next 5 months.")
    
    cell_2 = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
df = pd.read_excel('mothly.xlsx', header=None, names=['Month', 'Value'])

print("Data loaded successfully. Length:", len(df))
print(df.head())""")

    cell_3 = nbf.v4.new_markdown_cell("## SSA Class Definition\nHere we implement a robust SSA algorithm using numpy SVD, implementing Embedding, Reconstruction, and Forecasting via Linear Recurrent Formula (LRF).")

    cell_4 = nbf.v4.new_code_cell("""class SSA:
    def __init__(self, tseries, L):
        # Time series and Window Length L
        self.tseries = np.array(tseries)
        self.N = len(self.tseries)
        self.L = L
        self.K = self.N - self.L + 1
        
        # Step 1: Embedding (Trajectory Matrix)
        self.X = np.column_stack([self.tseries[i:i+self.L] for i in range(self.K)])
        
        # Step 2: Singular Value Decomposition (SVD)
        self.U, self.Sigma, self.VT = np.linalg.svd(self.X)
        self.d = np.linalg.matrix_rank(self.X)

    def reconstruct(self, components):
        # Step 3 & 4: Grouping and Diagonal Averaging
        if isinstance(components, int): components = [components]
        
        X_elem = np.zeros_like(self.X, dtype=float)
        for i in components:
            if i < len(self.Sigma):
                X_elem += self.Sigma[i] * np.outer(self.U[:, i], self.VT[i, :])
            
        rcs = np.zeros(self.N)
        counts = np.zeros(self.N)
        for i in range(self.L):
            for j in range(self.K):
                rcs[i+j] += X_elem[i, j]
                counts[i+j] += 1
        return rcs / counts

    def forecast(self, components, steps=5):
        # Step 5: Forecasting via Linear Recurrent Formula (LRF)
        if isinstance(components, int): components = [components]
        components = [c for c in components if c < len(self.Sigma)]
        
        U_m = self.U[:-1, components] # L-1 x r
        pi_m = self.U[-1, components] # r
        
        v_sq = np.sum(pi_m**2)
        if v_sq >= 1.0:
            print("Warning: LRF not stable for chosen components.")
            return np.zeros(steps)
            
        R = np.zeros(self.L - 1)
        for i, c in enumerate(components):
            R += pi_m[i] * U_m[:, i]
        R = R / (1 - v_sq)
        
        rec = self.reconstruct(components)
        predictions = list(rec)
        
        for _ in range(steps):
            last_window = np.array(predictions[-(self.L-1):])
            next_val = np.dot(R, last_window)
            predictions.append(next_val)
            
        return np.array(predictions[-steps:])""")

    cell_5 = nbf.v4.new_markdown_cell("## Execute SSA and Plot Results\nWe use window length $L=12$ for monthly data to capture annual seasonality. We extract Trend (Component 0), Seasonality (Components 1-3), and the rest is Noise. We print and plot a 5-month forecast.")

    cell_6 = nbf.v4.new_code_cell("""# Configuration
L = 12
steps_to_forecast = 5

# Initialize SSA
ssa = SSA(df['Value'], L=L)

# Extract components
trend = ssa.reconstruct(0)
seasonality = ssa.reconstruct([1, 2, 3])
noise = df['Value'] - trend - seasonality

# Forecast
forecast = ssa.forecast([0, 1, 2, 3], steps=steps_to_forecast)

# Generate Future Month Names
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
last_month_idx = months.index(df['Month'].iloc[-1].strip())
forecast_months = []
for i in range(1, steps_to_forecast + 1):
    forecast_months.append(months[(last_month_idx + i) % 12])

# Store in DataFrame
df['Trend'] = trend
df['Seasonality'] = seasonality
df['Noise'] = noise

# Plotting
fig, axes = plt.subplots(5, 1, figsize=(12, 20))
fig.tight_layout(pad=6.0)

x_ticks = range(len(df))

# Original
axes[0].plot(x_ticks, df['Value'], label='Original Data', color='black', alpha=0.7, marker='o')
axes[0].set_xticks(x_ticks)
axes[0].set_xticklabels(df['Month'], rotation=45)
axes[0].set_title('Original Time Series')
axes[0].legend()
axes[0].grid(True)

# Trend
axes[1].plot(x_ticks, df['Trend'], label='Trend (Comp 0)', color='red', marker='o')
axes[1].set_xticks(x_ticks)
axes[1].set_xticklabels(df['Month'], rotation=45)
axes[1].set_title('Trend')
axes[1].legend()
axes[1].grid(True)

# Seasonality
axes[2].plot(x_ticks, df['Seasonality'], label='Seasonality (Comps 1-3)', color='green', marker='o')
axes[2].set_xticks(x_ticks)
axes[2].set_xticklabels(df['Month'], rotation=45)
axes[2].set_title('Seasonality')
axes[2].legend()
axes[2].grid(True)

# Noise
axes[3].plot(x_ticks, df['Noise'], label='Noise', color='grey', alpha=0.5, marker='o')
axes[3].set_xticks(x_ticks)
axes[3].set_xticklabels(df['Month'], rotation=45)
axes[3].set_title('Noise')
axes[3].legend()
axes[3].grid(True)

# Forecast
forecast_x = range(len(df), len(df) + steps_to_forecast)
axes[4].plot(x_ticks, df['Value'], label='Historical Data', color='black', alpha=0.4, marker='o')
axes[4].plot(forecast_x, forecast, label='5-Month Forecast', color='blue', linestyle='--', marker='o')

all_x_ticks = list(x_ticks) + list(forecast_x)
all_labels = list(df['Month']) + forecast_months
axes[4].set_xticks(all_x_ticks)
axes[4].set_xticklabels(all_labels, rotation=45)

axes[4].set_title('5-Month Forecast')
axes[4].legend()
axes[4].grid(True)

# Save figure
plt.savefig('monthly_ssa_results.png', dpi=300, bbox_inches='tight')
plt.show()""")

    cell_7 = nbf.v4.new_markdown_cell("## 5-Month Forecast Values\nDisplaying the expected values for the next 5 months.")
    
    cell_8 = nbf.v4.new_code_cell("""# Create a DataFrame for the 5-month forecast and display it
forecast_df = pd.DataFrame({'Month': forecast_months, 'Forecast': forecast})
print(forecast_df.to_string(index=False))""")

    nb['cells'] = [cell_1, cell_2, cell_3, cell_4, cell_5, cell_6, cell_7, cell_8]
    
    with open('monthly_ssa_analysis.ipynb', 'w') as f:
        nbf.write(nb, f)
        
    print("Notebook 'monthly_ssa_analysis.ipynb' successfully generated.")

if __name__ == '__main__':
    build_notebook()
