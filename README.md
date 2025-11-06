# 📊 Trading212 → Yahoo Finance Portfolio Converter

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Export your Trading212 portfolio to Yahoo Finance in one click**

Seamlessly transfer your Trading212 positions to Yahoo Finance for advanced portfolio tracking, analysis, and performance monitoring. Automatic ticker conversion handles 13+ global exchanges including LSE, Euronext, NYSE, and NASDAQ.

---

## 📑 Table of Contents

- [Main Use Case](#-main-use-case)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Import to Yahoo Finance](#-how-to-import-to-yahoo-finance)
- [Supported Exchanges](#-supported-exchanges)
- [Example Output](#-example-output)
- [Screenshots](#-screenshots)
- [Advanced Usage](#️-advanced-usage)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Main Use Case

```
┌──────────────┐      ┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Trading212  │  →   │  This Tool  │  →   │ Yahoo Finance│  →   │   Track &    │
│  Portfolio   │      │  (1 click)  │      │     CSV      │      │   Analyze    │
│ 46 positions │      │  Transform  │      │  VUSA.L      │      │   Advanced   │
└──────────────┘      └─────────────┘      │  ADYEN.AS    │      │   Charts     │
                                            └──────────────┘      └──────────────┘
```

**Why?** Yahoo Finance offers superior portfolio analytics, charting, and tracking that Trading212's mobile app doesn't provide. This tool bridges the gap.

See the [complete flow diagram](.github/workflows/flow-diagram.md) for detailed architecture.

## ✨ Key Features

### 🚀 Core Functionality
- **One-Click Export** - Convert entire portfolio to Yahoo Finance CSV format
- **Smart Ticker Mapping** - Automatically handles exchange suffixes (.L, .AS, .F, .HK, etc.)
- **13+ Global Exchanges** - Supports LSE, Euronext, NYSE, NASDAQ, Frankfurt, Tokyo, and more
- **Accurate Metadata** - Uses instrument names, ISINs, and types for precise conversion

### 📈 Additional Features
- Portfolio tracking with unrealized P&L calculations
- Account balance and info retrieval
- Historical data export (organized by date)
- Smart caching (avoids API rate limits)
- Both demo and live environment support

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/t212.git
cd t212

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API credentials
cp .env.example .env
# Edit .env and add your Trading212 API key + secret
```

### Get Your API Credentials

1. Log into [Trading212](https://www.trading212.com/)
2. Go to Settings → API (Beta)
3. Generate API key + secret
4. Copy both to your `.env` file

### Run

```bash
python main.py
```

**Output:**
- `data/YYYY-MM-DD/yahoo/portfolio_HH-MM-SS.csv` ← **Import this to Yahoo Finance**
- `data/YYYY-MM-DD/portfolio/positions_HH-MM-SS.json` (backup)
- `data/YYYY-MM-DD/account/balance_HH-MM-SS.json` (account data)

## 📋 How to Import to Yahoo Finance

1. **Export from this tool**
   ```bash
   python main.py
   # Creates: data/2025-11-06/yahoo/portfolio_12-30-45.csv
   ```

2. **Import to Yahoo Finance**
   - Go to [Yahoo Finance](https://finance.yahoo.com/)
   - Click "My Portfolio" → Create New Portfolio
   - Click "Import" → "Upload from File"
   - Select your exported CSV file
   - Review and confirm

3. **Done!** 🎉
   - Track performance across all positions
   - View advanced charts and analytics
   - Monitor news and alerts
   - Compare against benchmarks

## 🌍 Supported Exchanges

<table>
<tr>
<td>

**🇬🇧 London**
- `.L` suffix
- Example: `VUSA.L`

**🇳🇱 Amsterdam**
- `.AS` suffix
- Example: `ADYEN.AS`

**🇫🇷 Paris**
- `.PA` suffix
- Example: `AI.PA`

**🇩🇪 Frankfurt**
- `.F` suffix
- Example: `SAP.F`

</td>
<td>

**🇺🇸 NYSE/NASDAQ**
- No suffix
- Example: `NVDA`, `AAPL`

**🇯🇵 Tokyo**
- `.T` suffix
- Example: `SONY.T`

**🇭🇰 Hong Kong**
- `.HK` suffix
- Example: `0700.HK`

**+ 6 more exchanges**
- Brussels, Madrid, Stockholm, Vienna, Zurich

</td>
</tr>
</table>

See [Exchange Mapping Guide](docs/EXCHANGE_MAPPING.md) for complete list.

## 🎨 Example Output

### Terminal Output
```
================================================================
Trading212 Application - DEMO Environment
================================================================

Fetching account balance...
================================================================
ACCOUNT BALANCE
================================================================
Free Cash........................          5,234.56
Total Value......................         52,847.91
Unrealised PnL...................         +3,421.18
Realised PnL.....................         +1,205.44
================================================================

Loading instrument metadata...
✓ Loaded 17,234 instruments (cached daily)

================================================================
PORTFOLIO - 46 Position(s)
================================================================

  Nvidia Corporation (NVDA STOCK)
  ISIN: US67066G1040
    Quantity................ 61.11
    Current Price........... 197.94
    Unrealised PnL.......... +10,034.52 (+120.52%)
...
```

### CSV Output (data/2025-11-06/yahoo/portfolio.csv)
```csv
Symbol,Current Price,Purchase Price,Quantity,Commission
NVDA,197.94,33.64,61.11,0.0
VUSA.L,98.60,98.45,10.16,0.0
ADYEN.AS,1403.70,1927.02,0.06,0.0
...
```

## 📸 Screenshots

> **Note**: Add screenshots here to showcase:
> 1. Terminal output showing portfolio export
> 2. Yahoo Finance import process
> 3. Final portfolio view in Yahoo Finance
>
> Screenshot locations: `assets/screenshots/`

<!-- Example placeholder for when screenshots are added:
### Export Process
![Terminal Output](assets/screenshots/terminal-output.png)

### Yahoo Finance Import
![Yahoo Import](assets/screenshots/yahoo-import.png)

### Final Result
![Portfolio Dashboard](assets/screenshots/yahoo-dashboard.png)
-->

## 🛠️ Advanced Usage

### Use as a Python Library

```python
from t212 import Trading212Client, export_portfolio_to_yahoo_csv

# Initialize client
client = Trading212Client(
    api_key="your_api_key",
    api_secret="your_api_secret",
    environment="demo"  # or "live"
)

# Get portfolio positions
positions = client.portfolio.get_all_positions()

# Export to Yahoo Finance CSV
instruments_list = client.instruments.get_all_instruments()
instruments = {inst['ticker']: inst for inst in instruments_list}
csv_path = export_portfolio_to_yahoo_csv(positions, instruments)

print(f"Exported to: {csv_path}")
# Output: Exported 46 positions to data/2025-11-06/yahoo/portfolio_12-30-45.csv
#         (3 with exchange suffix, 43 using shortName)
```

### Custom Integration

```python
# Get account balance
balance = client.account.get_cash()
print(f"Total: ${balance['total']:,.2f}")

# Get specific position
nvda = client.portfolio.get_position('NVDA_US_EQ')
print(f"NVDA: {nvda['quantity']} shares @ ${nvda['currentPrice']}")

# Search positions
apple_positions = client.portfolio.search_position('AAPL')
```

## 📊 Project Structure

```
t212/
├── t212/                     # Core library
│   ├── auth.py              # API authentication
│   ├── client.py            # HTTP client
│   ├── account.py           # Account endpoints
│   ├── portfolio.py         # Portfolio endpoints
│   ├── instruments.py       # Instrument metadata
│   └── utils.py             # Export & utilities
├── main.py                   # CLI application
├── data/                     # Output (auto-organized by date)
│   └── YYYY-MM-DD/
│       ├── yahoo/           # ← Yahoo Finance CSVs here
│       ├── portfolio/       # JSON backups
│       └── account/         # Account data
└── docs/                     # Documentation
    ├── EXCHANGE_MAPPING.md  # Exchange code reference
    ├── SETUP.md             # Detailed setup
    └── API_REFERENCE.md     # API documentation
```

## 🔧 Requirements

- **Python 3.7+**
- **Trading212 Account** (demo or live)
- **Trading212 API Credentials** (Settings → API Beta)

### Dependencies
```
requests>=2.31.0
python-dotenv>=1.0.0
```

## 🤝 Contributing

Contributions welcome! This is a personal project but happy to accept:
- Bug fixes
- Exchange mapping improvements
- New export formats
- Documentation updates

## 🔒 Security & Privacy

- ✅ Your API credentials stay **local** (never transmitted except to Trading212)
- ✅ All data stored **locally** in `data/` directory
- ✅ No external services or analytics
- ✅ Open source - audit the code yourself

**Best Practices:**
- Never commit `.env` file
- Use demo environment for testing
- Rotate API keys periodically
- Review exported data before sharing

## 📚 Documentation

- **[Exchange Mapping Guide](docs/EXCHANGE_MAPPING.md)** - Complete exchange code reference
- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[API Reference](docs/API_REFERENCE.md)** - Trading212 API endpoints
- **[Development Guide](CLAUDE.md)** - For contributors

## 🐛 Troubleshooting

<details>
<summary><b>Authentication errors (401)</b></summary>

- Verify both API key AND secret are set in `.env`
- Check you're using the correct environment (demo vs live)
- API credentials are environment-specific - demo keys won't work with live
</details>

<details>
<summary><b>Rate limiting errors (429)</b></summary>

- The tool uses smart caching to minimize API calls
- Instrument metadata cached daily (1 call per 50 seconds limit)
- Wait a minute and retry
</details>

<details>
<summary><b>Import errors in Python</b></summary>

- Ensure you're running from project root: `cd /path/to/t212`
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
</details>

<details>
<summary><b>Ticker not mapping correctly</b></summary>

- Check [Exchange Mapping Guide](docs/EXCHANGE_MAPPING.md) for supported exchanges
- Unrecognized exchange codes logged as warnings
- Report missing exchanges as GitHub issues
</details>

## ⭐ Star History

If this tool helped you, consider giving it a star! ⭐

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## ⚠️ Disclaimer

**This is an unofficial tool and is not affiliated with Trading212 or Yahoo Finance.**

- Use at your own risk
- No warranty or guarantees provided
- Author not responsible for financial losses
- Trading212 API is in beta and may change
- Always verify exported data before use

---

<div align="center">

**Built with ❤️ for the Trading212 community**

[Report Bug](https://github.com/yourusername/t212/issues) · [Request Feature](https://github.com/yourusername/t212/issues) · [Documentation](docs/)

</div>
