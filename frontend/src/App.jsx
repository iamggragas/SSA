import React, { useState, useRef } from 'react';
import axios from 'axios';
import { UploadCloud, TrendingUp, Calendar, FileText, Activity } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Brush
} from 'recharts';

function App() {
  const [file, setFile] = useState(null);
  const [forecastCount, setForecastCount] = useState(30);
  const [forecastType, setForecastType] = useState('daily');
  const [forecastDayOfWeek, setForecastDayOfWeek] = useState('Monday');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [isDragActive, setIsDragActive] = useState(false);
  
  const fileInputRef = useRef(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    setError('');
    setIsLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('forecast_periods', forecastCount);
    formData.append('forecast_type', forecastType);
    if (forecastType === 'day_of_week') {
      formData.append('forecast_day_of_week', forecastDayOfWeek);
    }
    
    try {
      const response = await axios.post('http://localhost:8000/api/forecast', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during forecasting.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDateLabel = (dateString) => {
    if (forecastType === 'daily' || !dateString) return dateString;
    const parts = dateString.split('-');
    if (parts.length >= 3) {
      const year = parts[0];
      const monthNum = parseInt(parts[1], 10);
      const dayNum = parseInt(parts[2], 10);
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      const monthName = (monthNum >= 1 && monthNum <= 12) ? months[monthNum - 1] : '';

      if (forecastType === 'monthly') {
        return `${monthName} ${year}`;
      } else if (forecastType === 'weekly') {
        const weekNum = Math.ceil(dayNum / 7);
        return `Week ${weekNum} (${monthName} ${year})`;
      }
    }
    return dateString;
  };

  const getCombinedChartData = () => {
    if (!result) return [];
    
    // Combine historical and forecast data for the chart
    const data = [];
    const { historical, forecast } = result;
    
    for (let i = 0; i < historical.dates.length; i++) {
      data.push({
        date: historical.dates[i],
        History: historical.values[i],
        Forecast: null
      });
    }
    
    for (let i = 0; i < forecast.dates.length; i++) {
      data.push({
        date: forecast.dates[i],
        History: null,
        Forecast: forecast.values[i]
      });
    }
    return data;
  };

  return (
    <div className="app-container">
      <header>
        <h1>SSA Forecaster</h1>
        <p className="subtitle">Advanced Time Series Forecasting using Singular Spectrum Analysis</p>
      </header>

      <div className="glass-panel">
        <form className="upload-form" onSubmit={handleSubmit}>
          
          {error && <div className="error-msg">{error}</div>}

          <div
            className={`upload-zone ${isDragActive ? 'drag-active' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
            onDragLeave={() => setIsDragActive(false)}
            onDrop={handleFileDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileSelect} 
              accept=".csv, .xlsx, .xls"
            />
            <UploadCloud size={48} className="upload-icon" />
            <div className="upload-text">
              {file ? file.name : "Drag and drop your Excel or CSV file here"}
            </div>
            {!file && <div className="upload-subtext">or click to browse from your computer</div>}
          </div>

          <div className="controls">
            <div className="input-group">
              <label><Calendar size={14} style={{display:'inline', marginRight:'4px', verticalAlign:'middle'}}/> Forecast Type</label>
              <select 
                className="input-field" 
                style={{ paddingRight: '30px' }}
                value={forecastType} 
                onChange={(e) => setForecastType(e.target.value)}
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="day_of_week">Specific Day</option>
              </select>
            </div>
            
            {forecastType === 'day_of_week' && (
              <div className="input-group">
                <label><Calendar size={14} style={{display:'inline', marginRight:'4px', verticalAlign:'middle'}}/> Select Day</label>
                <select 
                  className="input-field" 
                  value={forecastDayOfWeek} 
                  onChange={(e) => setForecastDayOfWeek(e.target.value)}
                >
                  <option value="Monday">Monday</option>
                  <option value="Tuesday">Tuesday</option>
                  <option value="Wednesday">Wednesday</option>
                  <option value="Thursday">Thursday</option>
                  <option value="Friday">Friday</option>
                  <option value="Saturday">Saturday</option>
                  <option value="Sunday">Sunday</option>
                </select>
              </div>
            )}
            
            <div className="input-group">
              <label><Calendar size={14} style={{display:'inline', marginRight:'4px', verticalAlign:'middle'}}/> Forecast {forecastType === 'daily' ? 'Days' : forecastType === 'weekly' ? 'Weeks' : forecastType === 'monthly' ? 'Months' : forecastDayOfWeek + 's'}</label>
              <input 
                type="number" 
                className="input-field" 
                value={forecastCount} 
                onChange={(e) => setForecastCount(e.target.value)}
                min="1"
                max={forecastType === 'daily' ? 365 : forecastType === 'monthly' ? 120 : 52}
              />
            </div>
            
            <button type="submit" className="btn-primary" disabled={isLoading || !file}>
              {isLoading ? (
                <><span className="loading-spinner" style={{marginRight: '8px'}}></span> Processing...</>
              ) : (
                <><TrendingUp size={16} style={{display:'inline', marginRight:'4px', verticalAlign:'middle'}}/> Run Forecast</>
              )}
            </button>
          </div>
        </form>
      </div>

      {result && (
        <>
          <div className="glass-panel">
            <h2 className="section-title"><Activity /> Visual Analysis</h2>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={getCombinedChartData()}
                  margin={{ top: 5, right: 30, left: 30, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#94a3b8" 
                    tick={{ fill: '#94a3b8' }} 
                    tickMargin={10}
                    minTickGap={30}
                    tickFormatter={formatDateLabel}
                    label={{ value: forecastType === 'day_of_week' ? forecastDayOfWeek + 's' : forecastType.charAt(0).toUpperCase() + forecastType.slice(1), position: 'bottom', offset: 35, fill: '#94a3b8', fontSize: 12 }}
                  />
                  <YAxis 
                    stroke="#94a3b8" 
                    tick={{ fill: '#94a3b8' }} 
                    label={{ value: 'Revenue', angle: -90, position: 'insideLeft', offset: -15, fill: '#94a3b8', fontSize: 12 }}
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    labelFormatter={formatDateLabel}
                  />
                  <Legend wrapperStyle={{ paddingTop: '40px' }} />
                  <Line 
                    type="monotone" 
                    dataKey="History" 
                    stroke="#94a3b8" 
                    strokeWidth={2} 
                    dot={false}
                    activeDot={{ r: 4 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="Forecast" 
                    stroke="#3b82f6" 
                    strokeWidth={3} 
                    dot={false}
                    activeDot={{ r: 6 }}
                  />
                  <Brush 
                    dataKey="date" 
                    height={30} 
                    stroke="#94a3b8" 
                    fill="rgba(15, 23, 42, 0.9)" 
                    tickFormatter={formatDateLabel} 
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-panel">
            <h2 className="section-title"><FileText /> Forecasted Data</h2>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>{forecastType === 'daily' ? 'Day' : forecastType === 'weekly' ? 'Week' : forecastType === 'monthly' ? 'Month' : forecastDayOfWeek}</th>
                    <th>Date</th>
                    <th>Predicted Value</th>
                  </tr>
                </thead>
                <tbody>
                  {result.forecast.dates.map((date, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{formatDateLabel(date)}</td>
                      <td>
                        <span style={{color: '#3b82f6', fontWeight: '600'}}>
                          {result.forecast.values[index].toFixed(4)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
