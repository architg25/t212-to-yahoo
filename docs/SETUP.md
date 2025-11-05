# Trading212 Client Setup Guide

## Prerequisites

- Python 3.7 or higher
- Trading212 account (live or demo)
- Trading212 API credentials (key + secret)

## Getting Your API Credentials

1. Log in to your Trading212 account
2. Navigate to Settings → API (Beta)
3. Generate a new API key pair
4. **Important**: Copy and save both the **API Key** and **API Secret** immediately - you won't be able to see them again

For detailed instructions, visit the [Trading212 Help Centre](https://helpcentre.trading212.com/hc/en-us/articles/14584770928157-Trading-212-API-key).

**Security Note**: Never commit your API credentials to version control or share them publicly.

## Installation

1. **Clone or navigate to the repository**
   ```bash
   cd /path/to/t212
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your API credentials:
   ```
   T212_API_KEY=your_actual_api_key_here
   T212_API_SECRET=your_actual_api_secret_here
   T212_ENV=demo  # or 'live' for production
   ```

## Usage

### Basic Usage

Run the application to fetch your account data:

```bash
python main.py
```

### Output

The application will:
1. Print your account balance and info to the console
2. Save data to `data/` with timestamped JSON files

Example console output:
```
============================================================
Trading212 Application - DEMO Environment
============================================================

Fetching account balance...

============================================================
ACCOUNT BALANCE
============================================================
Free Cash....................                      10,000.00
Total Value..................                      12,500.00
Unrealised PnL...............                      +1,500.00
Realised PnL.................                      +1,000.00
Cash Balance.................                      10,000.00
============================================================

✓ Balance saved to: data/2025-11-05/account/balance_22-10-30.json

Fetching account info...

============================================================
ACCOUNT INFO
============================================================
CURRENCYCODE.................                            USD
ID...........................                          12345
============================================================

✓ Info saved to: data/2025-11-05/account/info_22-10-30.json

Fetching portfolio positions...
Loading instrument metadata...
✓ Loaded 8247 instruments (cached daily)

================================================================================
PORTFOLIO - 2 Position(s)
================================================================================

  NVIDIA Corporation (NVDA)
  ISIN: US67066G1040
    Quantity................                    10.00
    Avg Price...............                   150.00
    Current Price...........                   155.00
    Position Value..........                 1,550.00
    Unrealised PnL..........                   +50.00 (+3.33%)

  Vanguard S&P 500 UCITS ETF (VUSA ETF)
  ISIN: IE00B3XXRP09
    Quantity................                     5.00
    Avg Price...............                    80.00
    Current Price...........                    85.00
    Position Value..........                   425.00
    Unrealised PnL..........                   +25.00 (+6.25%)

--------------------------------------------------------------------------------
  Total Portfolio Value...                 1,975.00
  Total Unrealised PnL....                   +75.00
================================================================================

✓ Portfolio saved to: data/2025-11-05/portfolio/positions_22-43-15.json

============================================================
SUCCESS
============================================================
```

## Switching Between Demo and Live

Edit your `.env` file:

**For demo/practice account:**
```
T212_ENV=demo
```

**For live/real account:**
```
T212_ENV=live
```

## Using the Python Package

You can also use the client programmatically:

```python
from t212 import Trading212Client

client = Trading212Client(
    api_key="your_api_key",
    api_secret="your_api_secret",
    environment="demo"
)

# Get account cash balance
balance = client.account.get_cash()
print(balance)

# Get account info
info = client.account.get_info()
print(info)
```

## Troubleshooting

### "T212_API_KEY and T212_API_SECRET required"
- Ensure you've created a `.env` file from `.env.example`
- Check that both your API key and secret are set correctly in `.env`
- Make sure you're running the script from the project root directory

### "Authentication failed. Check your API key and secret."
- Verify both your API key and secret are correct and haven't been revoked
- Check you're using the right environment (demo vs live)
- API credentials are environment-specific
- Make sure there are no extra spaces or quotes in your `.env` file

### "Access forbidden. Verify API key permissions."
- Your API key might not have the required permissions
- Try regenerating the API key pair with appropriate permissions

## Next Steps

- Check [API_REFERENCE.md](./API_REFERENCE.md) for available endpoints
- See [FEATURES.md](./FEATURES.md) for planned enhancements
