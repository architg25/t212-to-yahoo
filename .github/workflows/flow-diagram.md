# Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Trading212 Account                          │
│  Portfolio: 46 positions across NYSE, LSE, Euronext, etc.          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Trading212 API (REST)
                             │ • Account Balance
                             │ • Portfolio Positions
                             │ • Instrument Metadata
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     t212 Python Client                               │
│  • HTTP Basic Auth with API Key + Secret                           │
│  • Smart Caching (daily instrument metadata)                        │
│  • Ticker Transformation Engine                                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Automated Processing
                             │ • VUSAl_EQ → VUSA.L
                             │ • ADYENa_EQ → ADYEN.AS
                             │ • NVDA_US_EQ → NVDA
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Yahoo Finance Compatible CSV Export                     │
│  Symbol, Current Price, Purchase Price, Quantity, Commission        │
│  NVDA,197.94,33.64,61.11,0.0                                       │
│  VUSA.L,98.60,98.45,10.16,0.0                                      │
│  ADYEN.AS,1403.70,1927.02,0.06,0.0                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Manual Import
                             │ Yahoo Finance → My Portfolio → Import
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Yahoo Finance Portfolio                          │
│  • Advanced Charts & Analytics                                       │
│  • Performance Tracking                                              │
│  • News & Alerts                                                     │
│  • Benchmark Comparisons                                            │
└─────────────────────────────────────────────────────────────────────┘
```

## Why This Tool Exists

**Problem**: Trading212's mobile app has limited portfolio analytics
- No advanced charting
- Limited performance tracking
- No benchmark comparisons
- Basic P&L calculations

**Solution**: Yahoo Finance has superior portfolio tools
- Advanced technical analysis
- Customizable dashboards
- Historical performance charts
- News and alerts per position
- Compare against S&P 500, etc.

**Challenge**: Ticker format mismatch
- Trading212: `VUSAl_EQ`, `ADYENa_EQ`, `NVDA_US_EQ`
- Yahoo Finance: `VUSA.L`, `ADYEN.AS`, `NVDA`

**This Tool**: Bridges the gap automatically! 🎉
