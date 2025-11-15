#!/usr/bin/env python3
"""
Trading212 Application

Main application for interacting with Trading212 API.
"""

import os
import sys

from dotenv import load_dotenv

from t212 import Trading212Client, save_to_file, export_portfolio_to_yahoo_csv


def print_account_balance(data: dict):
    """Print account balance in a readable format."""

    # Map API keys to human-readable labels
    field_labels = {
        'free': 'Free Cash',
        'total': 'Total Value',
        'ppl': 'Unrealised PnL',
        'result': 'Realised PnL',
        'cash': 'Cash Balance'
    }

    print("\n" + "="*60)
    print("ACCOUNT BALANCE")
    print("="*60)

    for key, value in data.items():
        label = field_labels.get(key, key.upper())

        if isinstance(value, (int, float)):
            # Add +/- prefix for PnL fields
            if key in ['ppl', 'result']:
                sign = '+' if value >= 0 else ''
                print(f"{label:.<30} {sign}{value:>24,.2f}")
            else:
                print(f"{label:.<30} {value:>25,.2f}")
        else:
            print(f"{label:.<30} {value:>25}")

    print("="*60 + "\n")


def print_account_info(data: dict):
    """Print account info in a readable format."""
    print("\n" + "="*60)
    print("ACCOUNT INFO")
    print("="*60)

    for key, value in data.items():
        print(f"{key.upper():.<30} {value:>25}")

    print("="*60 + "\n")


def print_portfolio(positions: list, client: Trading212Client):
    """Print portfolio positions in a readable format with instrument metadata."""
    if not positions:
        print("\n" + "="*80)
        print("PORTFOLIO")
        print("="*80)
        print("No open positions")
        print("="*80 + "\n")
        return

    print("\n" + "="*80)
    print(f"PORTFOLIO - {len(positions)} Position(s)")
    print("="*80)
    print()

    # Fetch instrument metadata (cached to disk daily)
    print("Loading instrument metadata...")
    try:
        instruments_list = client.instruments.get_all_instruments()
        # Build lookup dict for fast access
        instruments = {inst['ticker']: inst for inst in instruments_list}
        print(f"✓ Loaded {len(instruments)} instruments (cached daily)\n")
    except Exception as e:
        print(f"⚠ Could not load instrument metadata: {e}")
        print("Displaying basic ticker information only\n")
        instruments = {}

    total_ppl = 0.0
    total_value = 0.0

    for pos in positions:
        ticker = pos.get('ticker', 'UNKNOWN')
        quantity = pos.get('quantity', 0)
        avg_price = pos.get('averagePrice', 0)
        current_price = pos.get('currentPrice', 0)
        ppl = pos.get('ppl', 0)

        position_value = quantity * current_price
        total_ppl += ppl
        total_value += position_value

        # Get instrument metadata
        instrument = instruments.get(ticker, {})
        name = instrument.get('name', ticker)
        short_name = instrument.get('shortName', ticker)
        isin = instrument.get('isin', 'N/A')
        instrument_type = instrument.get('type', 'STOCK')

        # Format display name with type if not a stock
        if instrument_type != 'STOCK':
            display_name = f"{name} ({short_name} {instrument_type})"
        else:
            display_name = f"{name} ({short_name})"

        # Format PnL with +/- sign
        ppl_sign = '+' if ppl >= 0 else ''
        ppl_percent = (ppl / (quantity * avg_price) * 100) if (quantity * avg_price) != 0 else 0
        ppl_percent_sign = '+' if ppl_percent >= 0 else ''

        print(f"  {display_name}")
        print(f"  ISIN: {isin}")
        print(f"    Quantity................ {quantity:>20,.2f}")
        print(f"    Avg Price............... {avg_price:>20,.2f}")
        print(f"    Current Price........... {current_price:>20,.2f}")
        print(f"    Position Value.......... {position_value:>20,.2f}")
        print(f"    Unrealised PnL.......... {ppl_sign}{ppl:>19,.2f} ({ppl_percent_sign}{ppl_percent:.2f}%)")
        print()

    print("-"*80)
    print(f"  Total Portfolio Value... {total_value:>20,.2f}")

    total_ppl_sign = '+' if total_ppl >= 0 else ''
    print(f"  Total Unrealised PnL.... {total_ppl_sign}{total_ppl:>19,.2f}")
    print("="*80 + "\n")


def fetch_account_data(client: Trading212Client, account: str = None):
    """Fetch and display all account data."""

    print("Fetching account balance...")
    balance = client.account.get_cash()
    print_account_balance(balance)

    balance_path = save_to_file(balance, "account", "balance", account=account)
    print(f"✓ Balance saved to: {balance_path}")

    print("\nFetching account info...")
    info = client.account.get_info()
    print_account_info(info)

    info_path = save_to_file(info, "account", "info", account=account)
    print(f"✓ Info saved to: {info_path}")

    print("\nFetching portfolio positions...")
    positions = client.portfolio.get_all_positions()
    print_portfolio(positions, client)

    portfolio_path = save_to_file(positions, "portfolio", "positions", account=account)
    print(f"✓ Portfolio saved to: {portfolio_path}")

    # Export to Yahoo Finance CSV (if there are positions)
    if positions:
        try:
            instruments_list = client.instruments.get_all_instruments()
            instruments = {inst['ticker']: inst for inst in instruments_list}
            export_portfolio_to_yahoo_csv(positions, instruments, account=account)
        except Exception as e:
            # Fallback to basic export without instrument metadata
            print(f"Warning: Could not load instrument metadata: {e}", file=sys.stderr)
            export_portfolio_to_yahoo_csv(positions, account=account)


def main():
    """Main application entry point."""
    load_dotenv()

    api_key = os.getenv('T212_API_KEY')
    api_secret = os.getenv('T212_API_SECRET')
    environment = os.getenv('T212_ENV', 'demo')
    account = os.getenv('T212_ACCOUNT')

    if not api_key or not api_secret:
        print("ERROR: T212_API_KEY and T212_API_SECRET required", file=sys.stderr)
        print("Copy .env.example to .env and set your credentials", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Trading212 Application - {environment.upper()} Environment")
    if account:
        print(f"Account: {account}")
    print(f"{'='*60}\n")

    try:
        client = Trading212Client(
            api_key=api_key,
            api_secret=api_secret,
            environment=environment
        )

        fetch_account_data(client, account=account)

        print("\n" + "="*60)
        print("SUCCESS")
        print("="*60 + "\n")

    except ValueError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nAPI ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
