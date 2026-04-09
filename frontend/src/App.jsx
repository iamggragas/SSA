import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RevenueForecaster from './pages/RevenueForecaster';
import InventoryForecaster from './pages/InventoryForecaster';
import { LayoutDashboard, Package } from 'lucide-react';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <nav className="sidebar">
          <div className="sidebar-header">
            <h2>SSA Analytics</h2>
          </div>
          <ul className="nav-links">
            <li>
              <Link to="/">
                <LayoutDashboard size={20} />
                <span>Revenue Forecaster</span>
              </Link>
            </li>
            <li>
              <Link to="/inventory">
                <Package size={20} />
                <span>Inventory Forecaster</span>
              </Link>
            </li>
          </ul>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<RevenueForecaster />} />
            <Route path="/inventory" element={<InventoryForecaster />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
