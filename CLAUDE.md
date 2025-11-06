# Trading212 API Client - Development Guide

This document provides instructions for working with the Trading212 API client codebase.

## Project Overview

Python client library for the Trading212 API with a modular architecture for easy extension.

**Current Features**: Account data, portfolio positions, and instrument metadata with smart caching

## Architecture

### Module Structure

```
t212/
├── __init__.py      # Package exports (Trading212Client, save_to_file)
├── auth.py          # HTTP Basic Auth handler
├── client.py        # Base HTTP client with request handling
├── account.py       # Account data endpoints (cash, info)
├── portfolio.py     # Portfolio endpoints (positions)
├── instruments.py   # Instruments metadata (names, ISINs) with disk caching
└── utils.py         # Utility functions (save_to_file)
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
# Edit .env with your demo credentials
```

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

- Official docs: https://docs.trading212.com/api
- Base URLs:
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

All output is organized by date for audit tracking:

```
data/
  2025-11-05/
    account/
      balance_22-43-15.json
      info_22-43-15.json
    portfolio/
      positions_22-43-15.json
    instruments/
      instruments.json
  2025-11-06/
    account/
      balance_09-30-00.json
    portfolio/
      positions_09-30-00.json
    instruments/
      instruments.json
  ...
```

**Note**: Historical data is never deleted automatically - manage disk space manually if needed.

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
