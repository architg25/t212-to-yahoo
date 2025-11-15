# Trading212 API Client - Development Guide

This document provides instructions for working with the Trading212 API client codebase.

## Project Overview

Python client library for the Trading212 API with a modular architecture for easy extension.

**Current Features**: Account data, portfolio positions, instrument metadata with smart caching, and Yahoo Finance CSV export

## Architecture

### Module Structure

```
t212/
├── __init__.py      # Package exports (Trading212Client, save_to_file, export_portfolio_to_yahoo_csv)
├── auth.py          # HTTP Basic Auth handler
├── client.py        # Base HTTP client with request handling
├── account.py       # Account data endpoints (cash, info)
├── portfolio.py     # Portfolio endpoints (positions)
├── instruments.py   # Instruments metadata (names, ISINs) with disk caching
└── utils.py         # Utility functions (save_to_file, export_portfolio_to_yahoo_csv)
```

### Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
   - `auth.py`: Authentication logic only
   - `client.py`: HTTP communication and base client setup
   - `account.py`: Account-specific API endpoints

2. **Easy Extension**: To add new API sections (e.g., orders, portfolio):
   - Create new module (e.g., `orders.py`)
   - Follow the pattern in `account.py`
   - Add to client as `self.orders = OrdersAPI(self)` in `client.py`

3. **Error Handling**: Centralized in `client.py` with specific exceptions for:
   - `401`: Authentication errors
   - `403`: Permission errors
   - `429`: Rate limiting
   - Network errors

## Development Setup

### Prerequisites

- Python 3.7+
- Trading212 demo account for testing
- API credentials (key + secret)

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your credentials:
#   - T212_API_KEY: Your API key
#   - T212_API_SECRET: Your API secret
#   - T212_ENV: 'demo' or 'live'
#   - T212_ACCOUNT (optional): Account identifier for file naming (e.g., ISA, INVEST, CFD)
```

### Environment Variables

- **T212_API_KEY** (required): Your Trading212 API key
- **T212_API_SECRET** (required): Your Trading212 API secret
- **T212_ENV** (optional): Environment (`demo` or `live`, defaults to `demo`)
- **T212_ACCOUNT** (optional): Account identifier appended to saved filenames
  - Examples: `ISA`, `INVEST`, `CFD`
  - Affects filenames: `balance_ISA_22-43-15.json`, `portfolio_ISA_22-43-15.json`, `portfolio_ISA_22-43-15.csv`
  - If not set, files are saved without account identifier

### Testing

Currently manual testing via `main.py`:

```bash
python main.py
```

**TODO**: Add automated tests (unit + integration)

## Adding New Features

### Example: Adding Orders API

1. **Create new module** (`t212/orders.py`):
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Trading212Client

class OrdersAPI:
    def __init__(self, client: 'Trading212Client'):
        self.client = client

    def get_all_pending(self) -> list:
        """Get all pending orders."""
        return self.client.get('/equity/orders')

    def place_market_order(self, ticker: str, quantity: float) -> dict:
        """Place a market order."""
        return self.client.post('/equity/orders/market', {
            'ticker': ticker,
            'quantity': quantity
        })
```

2. **Register in client** (`t212/client.py`):
```python
from .orders import OrdersAPI

class Trading212Client:
    def __init__(self, ...):
        # ... existing code ...
        self.account = AccountAPI(self)
        self.orders = OrdersAPI(self)  # Add this
```

3. **Export if needed** (`t212/__init__.py`):
```python
from .client import Trading212Client
from .orders import OrdersAPI

__all__ = ["Trading212Client", "OrdersAPI"]
```

### Code Style

- Type hints for all public methods
- Docstrings with rate limits, params, return types, examples
- Raise descriptive exceptions (ValueError for config, RuntimeError for API errors)
- Follow existing patterns in `account.py`

## API Reference

- **Official API Documentation**: https://docs.trading212.com/api
- **How to Get API Key**: https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-Trading-212-API-key
- **Base URLs**:
  - Demo: `https://demo.trading212.com/api/v0`
  - Live: `https://live.trading212.com/api/v0`

## Rate Limiting

All endpoints have rate limits. Document them in method docstrings:

```python
def get_cash(self) -> dict:
    """
    Get account cash balance.

    Rate Limit: 1 request per 2 seconds
    ...
    """
```

## Current Limitations

- No automated tests
- Account data, portfolio, and instruments endpoints only (no orders, history)
- No retry logic for rate limits
- Response caching only for instruments (disk + memory)

## Caching Strategy

### Instruments Cache
- **In-memory**: Fast lookup during application runtime
- **Disk**: Daily files (`data/YYYY-MM-DD/instruments/instruments.json`)
- **Retention**: All historical data is kept as an audit log
- **Rate limit**: 1 request per 50 seconds (caching avoids hitting limit)

## Data Organization

All output is organized by date for audit tracking. Files can optionally include an account identifier (set via `T212_ACCOUNT` environment variable):

```
data/
  2025-11-05/
    account/
      balance_ISA_22-43-15.json
      info_ISA_22-43-15.json
    portfolio/
      positions_ISA_22-43-15.json
    yahoo/
      portfolio_ISA_22-43-15.csv
    instruments/
      instruments.json
  2025-11-06/
    account/
      balance_ISA_09-30-00.json
    portfolio/
      positions_ISA_09-30-00.json
    yahoo/
      portfolio_ISA_09-30-00.csv
    instruments/
      instruments.json
  ...
```

**File Naming Convention**:
- With account: `filename_ACCOUNT_HH-MM-SS.json` (e.g., `balance_ISA_22-43-15.json`)
- Without account: `filename_HH-MM-SS.json` (e.g., `balance_22-43-15.json`)

**Note**: Historical data is never deleted automatically - manage disk space manually if needed.

## Yahoo Finance CSV Export

### Ticker Transformation

Trading212 tickers are automatically transformed to Yahoo Finance format using exchange suffix mapping:

1. **Check for exchange suffix**: If ticker ends with lowercase letter (e.g., `VUSAl_EQ`, `ADYENa_EQ`), map to Yahoo Finance exchange suffix
2. **Use shortName**: For tickers without exchange suffix (e.g., `NVDA_US_EQ`), use `shortName` from instrument metadata
3. **Fallback**: Extract prefix before underscore if instrument data unavailable

Implementation in `t212/utils.py:transform_ticker_for_yahoo()`

### Exchange Suffix Mapping

Trading212 uses lowercase letters to indicate exchanges. These are mapped to Yahoo Finance suffixes:

| Code | Exchange Name                 | Yahoo Suffix | Example Transformation |
|------|-------------------------------|--------------|------------------------|
| a    | Euronext Amsterdam            | .AS          | ADYENa_EQ → ADYEN.AS  |
| b    | Euronext Brussels             | .BR          | —                      |
| f    | Frankfurt (Xetra)             | .F           | —                      |
| g    | Euronext Paris                | .PA          | —                      |
| h    | Hong Kong                     | .HK          | —                      |
| l    | London Stock Exchange         | .L           | VUSAl_EQ → VUSA.L     |
| m    | Madrid Stock Exchange         | .MC          | —                      |
| n    | New York Stock Exchange       | .N           | —                      |
| o    | NASDAQ                        | .O           | —                      |
| s    | Stockholm (Nasdaq OMX)        | .ST          | —                      |
| t    | Tokyo Stock Exchange          | .T           | —                      |
| v    | Vienna Stock Exchange         | .VI          | —                      |
| z    | SIX Swiss Exchange (Zurich)   | .SW          | —                      |

**Usage Notes**:
- The instrument type suffix (`_EQ`, `_ETF`, etc.) is stripped before mapping
- The last lowercase letter of the ticker prefix indicates the exchange
- Unrecognized exchange codes are logged as warnings and use `.{UPPERCASE}` fallback
- US stocks (NYSE/NASDAQ) typically have no lowercase suffix and use shortName directly

### CSV Format

The exported CSV matches Yahoo Finance portfolio import format with these fields populated:
- **Symbol**: Transformed ticker
- **Current Price**: From `currentPrice` field (adjusted for GBX currency)
- **Date**: Yesterday's date in YYYY/MM/DD format
- **Time**: Fixed at `16:00 EST` (market close)
- **Purchase Price**: From `averagePrice` field
- **Quantity**: From `quantity` field
- **Commission**: Default `0.0`

**Position Sorting**: Positions are sorted by current value (`currentPrice × quantity`) in ascending order (smallest to largest). GBX (pence) prices are automatically divided by 100 before calculating position value.

**Currency Handling**: The export automatically detects GBX (pence) currency codes from instrument metadata and divides prices by 100 to convert to pounds for accurate position calculations.

Other fields (Change, Open, High, Low, Volume, Trade Date, etc.) are left empty as they're not available from Trading212 API.

### Usage

```python
from t212 import export_portfolio_to_yahoo_csv

# Fetch positions
positions = client.portfolio.get_all_positions()

# Fetch instruments for proper ticker transformation and currency handling
instruments_list = client.instruments.get_all_instruments()
instruments = {inst['ticker']: inst for inst in instruments_list}

# Export to Yahoo Finance CSV
csv_path = export_portfolio_to_yahoo_csv(positions, instruments, account="ISA")
# Saves to: data/2025-11-05/yahoo/portfolio_ISA_22-43-15.csv
```

The `main.py` application automatically exports the CSV when fetching portfolio data, using cached instrument metadata for accurate ticker transformation and currency handling. The account identifier is read from the `T212_ACCOUNT` environment variable.

## Roadmap

See [docs/FEATURES.md](docs/FEATURES.md) for planned features.

Priority areas:
1. Order placement and management
2. Historical data (orders, dividends, transactions)
3. Advanced analytics and reporting

## Building & Running

### Application

Run the main application:

```bash
python main.py
```

### Using the Library

The `t212/` package can be imported and used in any Python code:

```python
from t212 import Trading212Client

client = Trading212Client(
    api_key="your_key",
    api_secret="your_secret",
    environment="demo"
)

balance = client.account.get_cash()
```

## Troubleshooting

### Import Errors

Make sure you're running from the project root:
```bash
cd /path/to/t212
python main.py
```

### Authentication Failures

- Check both API key AND secret are set in `.env`
- Verify you're using the right environment (demo vs live)
- API credentials are environment-specific

## Notes

- Always test with demo environment first
- Never commit `.env` file
- API is in beta - endpoints may change
- Market orders only supported in live environment

## Code Quality Improvements

### Recent Enhancements (2025-11-06)

1. **Better Type Hints**:
   - Added `Optional[Dict]` for instrument parameters
   - Consistent typing across all utility functions
   - Explicit `__all__` exports in utils module

2. **Module-Level Constants**:
   - `EXCHANGE_SUFFIXES` moved to module level for reusability
   - Imports organized at top of file (no mid-function imports)

3. **Export Statistics**:
   - `export_portfolio_to_yahoo_csv()` now prints detailed summary
   - Reports count of exchange-mapped vs shortName-mapped tickers
   - Validates non-empty positions before export

4. **Error Handling**:
   - Better error messages with context
   - Graceful fallback when instruments API unavailable
   - Warnings for unrecognized exchange codes

5. **Documentation**:
   - Comprehensive exchange mapping table in `docs/EXCHANGE_MAPPING.md`
   - Clear transformation examples
   - Usage notes for edge cases
