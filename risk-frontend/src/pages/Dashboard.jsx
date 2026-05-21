import React, { useState } from "react";
import API from "../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function Dashboard() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    if (!ticker) return;

    setLoading(true);

    try {
      // Fetch market data
      const res = await API.get(`/market/${ticker}`);

      console.log("Market Response:", res.data);

      // Validate backend response
      if (!res.data || !res.data.dates || !res.data.prices) {
        alert("Invalid data returned from backend");
        setLoading(false);
        return;
      }

      setData(res.data);

      // Fetch risk metrics
      const riskRes = await API.post("/risk/metrics", {
        prices: res.data.prices,
      });

      console.log("Risk Response:", riskRes.data);

      setRisk(riskRes.data);

    } catch (err) {
      console.error(err);
      alert("Error fetching market data");
    }

    setLoading(false);
  };

  // Chart data preparation
  const chartData =
    data && data.dates && data.prices
      ? data.dates.map((date, i) => ({
          date,
          price: data.prices[i],
        }))
      : [];

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Risk Analytics Dashboard</h1>

      {/* Input Section */}
      <div style={{ marginBottom: 20 }}>
        <input
          type="text"
          placeholder="Enter ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          style={{
            padding: "10px",
            width: "250px",
            marginRight: "10px",
          }}
        />

        <button
          onClick={fetchData}
          style={{
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          Fetch Data
        </button>
      </div>

      {/* Loading */}
      {loading && <p>Loading...</p>}

      {/* Risk Metrics */}
      {risk && (
        <div
          style={{
            marginTop: 20,
            padding: 20,
            border: "1px solid #ddd",
            borderRadius: 10,
            width: "400px",
          }}
        >
          <h3>Risk Metrics</h3>

          <p>
            <strong>Volatility:</strong>{" "}
            {risk.volatility?.toFixed(4)}
          </p>

          <p>
            <strong>Sharpe Ratio:</strong>{" "}
            {risk.sharpe_ratio != null
              ? risk.sharpe_ratio.toFixed(4)
              : "N/A"}
          </p>

          <p>
            <strong>Value at Risk (95%):</strong>{" "}
            {risk.var_95?.toFixed(4)}
          </p>

          <p>
            <strong>Average Annual Return:</strong>{" "}
            {risk.avg_return?.toFixed(4)}
          </p>
        </div>
      )}

      {/* Chart */}
      {chartData.length > 0 && (
        <div style={{ marginTop: 40 }}>
          <h3>{data.ticker} Closing Prices</h3>

          <LineChart
            width={900}
            height={400}
            data={chartData}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="date" hide />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="price"
              stroke="#007bff"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </div>
      )}
    </div>
  );
}