"""
Utility functions for the Trading212 API client.
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

__all__ = [
    'save_to_file',
    'transform_ticker_for_yahoo',
    'export_portfolio_to_yahoo_csv',
    'EXCHANGE_SUFFIXES'
]

# Exchange suffix mapping for Trading212 to Yahoo Finance format
EXCHANGE_SUFFIXES = {
    'a': '.AS',  # Euronext Amsterdam
    'b': '.BR',  # Euronext Brussels
    'f': '.F',   # Frankfurt (Xetra)
    'g': '.PA',  # Euronext Paris
    'h': '.HK',  # Hong Kong
    'l': '.L',   # London Stock Exchange
    'm': '.MC',  # Madrid Stock Exchange
    'n': '.N',   # New York Stock Exchange
    'o': '.O',   # NASDAQ
    's': '.ST',  # Stockholm (Nasdaq OMX)
    't': '.T',   # Tokyo Stock Exchange
    'v': '.VI',  # Vienna Stock Exchange
    'z': '.SW',  # SIX Swiss Exchange (Zurich)
}


def save_to_file(
    data: Union[dict, list],
    category: str,
    filename: str,
    base_dir: Path = Path("data")
) -> Path:
    """
    Save data to a date-organized JSON file.

    Structure: data/YYYY-MM-DD/category/filename_HH-MM-SS.json

    Args:
        data: Data to save (dict or list)
        category: Category folder (e.g., 'account', 'portfolio', 'instruments')
        filename: Base filename (e.g., 'balance', 'positions')
        base_dir: Base directory (default: 'data')

    Returns:
        Path: Path to the saved file

    Example:
        >>> from t212.utils import save_to_file
        >>> balance = client.account.get_cash()
        >>> path = save_to_file(balance, "account", "balance")
        >>> print(path)
        data/2025-11-05/account/balance_22-43-15.json
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    # Create directory structure: data/YYYY-MM-DD/category/
    directory = base_dir / date_str / category
    directory.mkdir(parents=True, exist_ok=True)

    # Filename: filename_HH-MM-SS.json
    full_filename = f"{filename}_{time_str}.json"
    filepath = directory / full_filename

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return filepath


def transform_ticker_for_yahoo(ticker: str, instrument: Optional[Dict] = None) -> str:
    """
    Transform Trading212 ticker to Yahoo Finance format.

    Rules:
    1. Check ticker prefix for lowercase exchange suffix and map to Yahoo Finance format
    2. For tickers without exchange suffix, use shortName from instrument metadata
    3. Fallback: Extract prefix before underscore

    Exchange Suffix Mapping (see EXCHANGE_SUFFIXES constant):
        a → .AS  (Euronext Amsterdam)
        b → .BR  (Euronext Brussels)
        f → .F   (Frankfurt/Xetra)
        g → .PA  (Euronext Paris)
        h → .HK  (Hong Kong)
        l → .L   (London Stock Exchange)
        m → .MC  (Madrid Stock Exchange)
        n → .N   (New York Stock Exchange)
        o → .O   (NASDAQ)
        s → .ST  (Stockholm/Nasdaq OMX)
        t → .T   (Tokyo Stock Exchange)
        v → .VI  (Vienna Stock Exchange)
        z → .SW  (SIX Swiss Exchange/Zurich)

    Args:
        ticker: Trading212 ticker (e.g., 'NVDA_US_EQ', 'VUSAl_EQ', 'ADYENa_EQ')
        instrument: Optional instrument metadata dict

    Returns:
        str: Yahoo Finance ticker (e.g., 'NVDA', 'VUSA.L', 'ADYEN.AS')

    Examples:
        >>> transform_ticker_for_yahoo('NVDA_US_EQ', {'shortName': 'NVDA', 'type': 'STOCK'})
        'NVDA'
        >>> transform_ticker_for_yahoo('VUSAl_EQ', {'shortName': 'VUSA', 'type': 'ETF'})
        'VUSA.L'
        >>> transform_ticker_for_yahoo('ADYENa_EQ', {'shortName': 'ADYEN', 'type': 'STOCK'})
        'ADYEN.AS'
    """
    # Extract prefix before underscore
    prefix = ticker.split('_')[0]

    # Check if prefix ends with lowercase letter (exchange indicator)
    if prefix and prefix[-1].islower():
        suffix_char = prefix[-1]
        exchange_code = EXCHANGE_SUFFIXES.get(suffix_char)

        if exchange_code:
            # Known exchange code - use mapping
            return prefix[:-1] + exchange_code
        else:
            # Unrecognized exchange code - log warning and use uppercase fallback
            print(
                f"Warning: Unrecognized exchange code '{suffix_char}' in ticker '{ticker}'. "
                f"Using .{suffix_char.upper()} fallback.",
                file=sys.stderr
            )
            return prefix[:-1] + f'.{suffix_char.upper()}'

    # No exchange suffix - use shortName if available
    if instrument:
        short_name = instrument.get('shortName', '')
        if short_name:
            return short_name

    return prefix


def export_portfolio_to_yahoo_csv(
    positions: list,
    instruments: Optional[Dict[str, dict]] = None,
    output_path: Optional[Path] = None,
    base_dir: Path = Path("data")
) -> Path:
    """
    Export portfolio positions to Yahoo Finance CSV format.

    Structure: data/YYYY-MM-DD/yahoo/portfolio_HH-MM-SS.csv

    Args:
        positions: List of position dicts from Trading212 API
        instruments: Optional dict mapping ticker to instrument metadata
        output_path: Optional custom output path
        base_dir: Base directory (default: 'data')

    Returns:
        Path: Path to the saved CSV file

    Raises:
        ValueError: If positions list is empty

    Example:
        >>> positions = client.portfolio.get_all_positions()
        >>> instruments_list = client.instruments.get_all_instruments()
        >>> instruments = {inst['ticker']: inst for inst in instruments_list}
        >>> path = export_portfolio_to_yahoo_csv(positions, instruments)
        >>> print(path)
        data/2025-11-05/yahoo/portfolio_22-30-15.csv
    """
    if not positions:
        raise ValueError("Cannot export empty positions list")

    # Use custom path or generate date-based path
    if output_path is None:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")

        directory = base_dir / date_str / "yahoo"
        directory.mkdir(parents=True, exist_ok=True)

        filename = f"portfolio_{time_str}.csv"
        output_path = directory / filename

    # Yahoo Finance CSV headers
    headers = [
        'Symbol', 'Current Price', 'Date', 'Time', 'Change', 'Open', 'High', 'Low',
        'Volume', 'Trade Date', 'Purchase Price', 'Quantity', 'Commission',
        'High Limit', 'Low Limit', 'Comment', 'Transaction Type'
    ]

    # Track transformations
    exchange_mapped = 0
    shortname_used = 0

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for pos in positions:
            ticker = pos.get('ticker', '')

            # Get instrument metadata if available
            instrument = instruments.get(ticker) if instruments else None

            # Track transformation type
            prefix = ticker.split('_')[0]
            if prefix and prefix[-1].islower():
                exchange_mapped += 1
            elif instrument and instrument.get('shortName'):
                shortname_used += 1

            yahoo_ticker = transform_ticker_for_yahoo(ticker, instrument)

            row = {
                'Symbol': yahoo_ticker,
                'Current Price': pos.get('currentPrice', ''),
                'Date': '',
                'Time': '',
                'Change': '',
                'Open': '',
                'High': '',
                'Low': '',
                'Volume': '',
                'Trade Date': '',
                'Purchase Price': pos.get('averagePrice', ''),
                'Quantity': pos.get('quantity', ''),
                'Commission': '0.0',
                'High Limit': '',
                'Low Limit': '',
                'Comment': '',
                'Transaction Type': ''
            }

            writer.writerow(row)

    # Print summary to stderr for logging
    print(
        f"Exported {len(positions)} positions to {output_path} "
        f"({exchange_mapped} with exchange suffix, {shortname_used} using shortName)",
        file=sys.stderr
    )

    return output_path
