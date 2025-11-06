# Exchange Suffix Mapping

This document describes how Trading212 ticker symbols are transformed to Yahoo Finance format.

## Overview

Trading212 uses lowercase letters at the end of ticker symbols to indicate the exchange. When exporting to Yahoo Finance CSV format, these need to be converted to the standard Yahoo Finance exchange suffixes.

## Mapping Table

| Code | Exchange Name                 | Standard Suffix | Example                    |
|------|-------------------------------|-----------------|----------------------------|
| a    | Euronext Amsterdam            | .AS             | ADYENa_EQ → ADYEN.AS      |
| b    | Euronext Brussels             | .BR             | —                          |
| f    | Frankfurt (Xetra)             | .F              | —                          |
| g    | Euronext Paris                | .PA             | —                          |
| h    | Hong Kong                     | .HK             | —                          |
| l    | London Stock Exchange         | .L              | VUSAl_EQ → VUSA.L         |
| m    | Madrid Stock Exchange         | .MC             | —                          |
| n    | New York Stock Exchange       | .N              | —                          |
| o    | NASDAQ                        | .O              | —                          |
| s    | Stockholm (Nasdaq OMX)        | .ST             | —                          |
| t    | Tokyo Stock Exchange          | .T              | —                          |
| v    | Vienna Stock Exchange         | .VI             | —                          |
| z    | SIX Swiss Exchange (Zurich)   | .SW             | —                          |

## Usage Notes

1. **Strip trailing instrument-type suffix** before mapping (e.g., `_EQ`, `_ETF`)
2. **Match the last lowercase letter** of the raw ticker (e.g., `ADYENa` → code `a`)
3. **Concatenate** the base symbol + mapped suffix to form a valid ticker (e.g., `ADYEN.AS`)
4. **Unrecognized codes** are logged as warnings and use `.{UPPERCASE}` fallback
5. **US stocks** (NYSE/NASDAQ) typically have no lowercase suffix and use shortName directly

## Transformation Algorithm

```python
def transform_ticker_for_yahoo(ticker: str, instrument: dict = None) -> str:
    """
    1. Extract prefix before underscore: VUSAl_EQ → VUSAl
    2. Check if ends with lowercase letter:
       - Yes: Map to exchange suffix (l → .L)
       - No: Use shortName from instrument metadata
    3. Return transformed ticker: VUSA.L
    """
```

## Examples

### With Exchange Suffix
- `VUSAl_EQ` → `VUSA.L` (London Stock Exchange)
- `ADYENa_EQ` → `ADYEN.AS` (Euronext Amsterdam)
- `EQQQl_EQ` → `EQQQ.L` (London Stock Exchange)

### Without Exchange Suffix (US Markets)
- `NVDA_US_EQ` → `NVDA` (uses shortName: NVDA)
- `AAPL_US_EQ` → `AAPL` (uses shortName: AAPL)
- `TSLA_US_EQ` → `TSLA` (uses shortName: TSLA)

## Implementation

The transformation logic is implemented in:
- **Module**: `t212/utils.py`
- **Function**: `transform_ticker_for_yahoo(ticker, instrument)`

This function is automatically called by `export_portfolio_to_yahoo_csv()` when generating Yahoo Finance CSV exports.
