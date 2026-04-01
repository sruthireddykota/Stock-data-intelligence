# Stock Data Intelligence

A comprehensive stock market analysis platform that provides real-time data, insights, and visualizations for Indian stocks. Built with FastAPI backend and Streamlit dashboard.

## Features

- **Real-time Stock Data**: Fetch historical and current stock data using Yahoo Finance
- **Advanced Analytics**: Generate moving averages, volatility metrics, and trend analysis
- **Stock Comparison**: Compare multiple stocks side-by-side
- **Interactive Dashboard**: Beautiful Streamlit interface for data visualization
- **RESTful API**: FastAPI-powered endpoints for programmatic access
- **Docker Support**: Containerized deployment with health checks
- **Indian Market Support**: Native support for NSE stocks (.NS suffix)

##  API Endpoints

### Health Check
- `GET /health` - Service health status

### Data Endpoints
- `GET /data/close?symbol=TCS.NS&start=2023-01-01&end=2023-12-31` - Volume and close price data
- `GET /data/summary?symbol=TCS.NS&period=13mo` - Technical indicators and metrics

### Insights & Analysis
- `GET /insights/{symbol}?period=13mo` - Key insights and metrics for a stock
- `GET /compare?symbol1=TCS.NS&symbol2=INFY.NS&period=13mo` - Compare two stocks

##  Installation

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-data-intelligence
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**
   ```bash
   uvicorn stocks_fastapi:app --host 0.0.0.0 --port 8010 --reload
   ```

5. **Run the Streamlit dashboard** (in a new terminal)
   ```bash
   streamlit run main.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the services**
   - FastAPI API: http://localhost:8010
   - Streamlit Dashboard: http://localhost:8511
   - API Documentation: http://localhost:8010/docs

##  Usage

### API Usage Examples

#### Get Stock Insights
```bash
curl "http://localhost:8010/insights/TCS.NS?period=13mo"
```

#### Compare Two Stocks
```bash
curl "http://localhost:8010/compare?symbol1=TCS.NS&symbol2=INFY.NS&period=13mo"
```

#### Get Historical Data
```bash
curl "http://localhost:8010/data/close?symbol=TCS.NS&start=2023-01-01&end=2023-12-31"
```

### Dashboard Features

The Streamlit dashboard provides:
- **Company Selection**: Choose from popular Indian IT stocks (INFY, TCS, WIPRO, TECHM)
- **Period Selection**: Analyze data for 1, 2, or 3-year periods
- **Key Metrics**: Latest close, 52-week high/low, trend, and risk indicators
- **Volume & Price Charts**: Interactive line charts for volume and closing prices
- **Stock Comparison**: Side-by-side comparison with moving average plots

## 🏗️ Project Structure

```
stock-data-intelligence/
├── data_pipeline.py          # Core data fetching and analysis logic
├── stocks_fastapi.py         # FastAPI application with endpoints
├── main.py                   # Streamlit dashboard application
├── requirements.txt          # Python dependencies
├── Dockerfile.fastapi        # FastAPI service container
├── Dockerfile.dashboard      # Streamlit dashboard container
├── docker-compose.yaml       # Multi-service orchestration
├── utils/
│   └── logger.py            # Logging utilities
└── logs/                    # Application logs
```

##  Configuration

### Environment Variables
Create a `.env` file for dashboard configuration:
```
# Add your environment variables here
```

### Supported Stock Symbols
- **Indian Stocks**: Use `.NS` suffix (e.g., `TCS.NS`, `INFY.NS`)
- **International Stocks**: Standard symbols (e.g., `AAPL`, `GOOGL`)

### Time Periods
- `13mo` - 1 year (13 months)
- `25mo` - 2 years (25 months)
- `37mo` - 3 years (37 months)


##  Data Sources

- **Yahoo Finance**: Primary data source via `yfinance` library
- **NSE India**: Indian stock market data (accessed through Yahoo Finance)


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Yahoo Finance for market data
- FastAPI and Streamlit communities
- Contributors and maintainers


