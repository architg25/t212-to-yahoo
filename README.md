# Trading212 Account Data Client

Simple Python client for fetching account data from the Trading212 API.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API credentials**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key + secret
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Features

- ✅ HTTP Basic Auth with API key + secret
- ✅ Modular structure (separate auth, client, account, portfolio, instruments modules)
- ✅ Fetch account balance/cash and account info
- ✅ Fetch portfolio positions with PnL calculations
- ✅ Instrument metadata (names, ISINs) with disk caching
- ✅ Support for demo and live environments
- ✅ Export data to JSON with timestamps
- ✅ Clean console output with formatted tables
- ✅ Smart caching (in-memory + daily disk cache)
- ✅ Programmatic API for custom integrations

## Project Structure

```
.
├── t212/                # Core library (API client)
│   ├── __init__.py      # Package exports
│   ├── auth.py          # HTTP Basic Auth handler
│   ├── client.py        # Base API client
│   ├── account.py       # Account data endpoints
│   ├── portfolio.py     # Portfolio endpoints
│   ├── instruments.py   # Instruments metadata (with caching)
│   └── utils.py         # Utility functions
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── data/                # JSON output (organized by date)
│   └── YYYY-MM-DD/      # Daily folders
│       ├── account/     # Account data
│       ├── portfolio/   # Portfolio snapshots
│       └── instruments/ # Cached instruments
└── docs/
    ├── SETUP.md         # Detailed setup guide
    ├── API_REFERENCE.md # Trading212 API documentation
    └── FEATURES.md      # Feature roadmap
```

**Architecture**:
- `t212/` - Reusable library for Trading212 API
- `main.py` - Your application that uses the library
- As you add features, expand `main.py` or create additional modules

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[API Reference](docs/API_REFERENCE.md)** - Trading212 API endpoints
- **[Features & Roadmap](docs/FEATURES.md)** - Current and planned features

## Requirements

- Python 3.7+
- Trading212 account (demo or live)
- Trading212 API credentials (key + secret)

## Usage as a Library

```python
from t212 import Trading212Client, save_to_file

client = Trading212Client(
    api_key="your_api_key",
    api_secret="your_api_secret",
    environment="demo"
)

# Get account cash
balance = client.account.get_cash()

# Get account info
info = client.account.get_info()

# Get portfolio positions
positions = client.portfolio.get_all_positions()

# Get specific position
position = client.portfolio.get_position('AAPL_US_EQ')

# Save data to organized structure
path = save_to_file(balance, "account", "balance")
# Saves to: data/2025-11-05/account/balance_22-30-15.json
```

## Security

- Never commit your `.env` file
- Keep your API credentials secure
- Use demo environment for testing

## License

MIT

## Disclaimer

This is an unofficial client. Use at your own risk. The author is not responsible for any financial losses incurred through the use of this software.
