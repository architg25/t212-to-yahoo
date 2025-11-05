"""
Instruments Metadata API endpoints.

Provides access to tradable instruments and exchange information.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import Trading212Client


class InstrumentsAPI:
    """
    Instruments Metadata API.

    Discover what you can trade. Access comprehensive lists of all tradable
    instruments and exchanges, including details like tickers, names, ISINs,
    and trading hours.
    """

    def __init__(self, client: 'Trading212Client'):
        """
        Initialize the Instruments API.

        Args:
            client: The main Trading212Client instance
        """
        self.client = client
        self._instruments_cache: Optional[list] = None
        self._exchanges_cache: Optional[list] = None
        self.data_dir = Path("data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_instruments_file_path(self) -> Path:
        """Get the file path for today's instruments cache."""
        today = datetime.now().strftime("%Y-%m-%d")
        instruments_dir = self.data_dir / today / "instruments"
        instruments_dir.mkdir(parents=True, exist_ok=True)
        return instruments_dir / "instruments.json"

    def _load_instruments_from_file(self) -> Optional[list]:
        """Load instruments from today's cache file if it exists."""
        file_path = self._get_instruments_file_path()
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _save_instruments_to_file(self, instruments: list):
        """Save instruments to today's cache file."""
        file_path = self._get_instruments_file_path()
        try:
            with open(file_path, 'w') as f:
                json.dump(instruments, f, indent=2)
        except Exception:
            pass

    def _cleanup_old_instrument_files(self):
        """Remove old date directories, keeping only today's."""
        today = datetime.now().strftime("%Y-%m-%d")

        # Iterate through date directories (YYYY-MM-DD format)
        if self.data_dir.exists():
            for date_dir in self.data_dir.iterdir():
                if date_dir.is_dir() and date_dir.name != today:
                    # Check if it looks like a date directory (YYYY-MM-DD)
                    if len(date_dir.name) == 10 and date_dir.name.count('-') == 2:
                        try:
                            # Remove the entire old date directory
                            import shutil
                            shutil.rmtree(date_dir)
                        except Exception:
                            pass

    def get_all_instruments(self, use_cache: bool = True) -> list:
        """
        Fetch all instruments that your account has access to.

        Rate Limit: 1 request per 50 seconds

        IMPORTANT: This endpoint has a strict rate limit. The results are
        cached to disk (one file per day) and in memory to avoid hitting
        the limit. Set use_cache=False to force a fresh fetch.

        Cache Strategy:
        1. Check in-memory cache
        2. Check disk cache (data/instruments_YYYY-MM-DD.json)
        3. Fetch from API if needed
        4. Save to disk and memory

        Args:
            use_cache: If True, return cached data if available (default: True)

        Returns:
            list: List of all available instruments, each containing:
                - ticker: Instrument ticker (e.g., 'AAPL_US_EQ')
                - name: Human-readable name (e.g., 'Apple Inc.')
                - isin: International Securities Identification Number
                - type: Instrument type (e.g., 'STOCK', 'ETF')
                - currencyCode: Trading currency
                - exchange: Exchange code
                - minTradeQuantity: Minimum quantity for trading
                - maxOpenQuantity: Maximum open quantity allowed
                - ... (other fields may be present)

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> instruments = client.instruments.get_all_instruments()
            >>> apple = [i for i in instruments if i['ticker'] == 'AAPL_US_EQ'][0]
            >>> print(apple['name'])  # 'Apple Inc.'
            >>> print(apple['isin'])  # 'US0378331005'
        """
        # Check in-memory cache
        if use_cache and self._instruments_cache is not None:
            return self._instruments_cache

        # Check disk cache
        if use_cache:
            cached_instruments = self._load_instruments_from_file()
            if cached_instruments is not None:
                self._instruments_cache = cached_instruments
                return cached_instruments

        # Fetch from API
        instruments = self.client.get('/equity/metadata/instruments')
        self._instruments_cache = instruments

        # Save to disk
        self._save_instruments_to_file(instruments)
        self._cleanup_old_instrument_files()

        return instruments

    def get_all_exchanges(self, use_cache: bool = True) -> list:
        """
        Fetch all exchanges and their working schedules.

        Rate Limit: 1 request per 30 seconds

        Args:
            use_cache: If True, return cached data if available (default: True)

        Returns:
            list: List of all exchanges with their working schedules

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> exchanges = client.instruments.get_all_exchanges()
        """
        if use_cache and self._exchanges_cache is not None:
            return self._exchanges_cache

        exchanges = self.client.get('/equity/metadata/exchanges')
        self._exchanges_cache = exchanges
        return exchanges

    def find_instrument(self, ticker: str) -> Optional[dict]:
        """
        Find a specific instrument by ticker.

        This is a convenience method that searches the cached instruments list.
        If the cache is empty, it will fetch all instruments first.

        Args:
            ticker: Instrument ticker to search for (e.g., 'AAPL_US_EQ')

        Returns:
            dict: Instrument data if found, None otherwise

        Example:
            >>> apple = client.instruments.find_instrument('AAPL_US_EQ')
            >>> if apple:
            ...     print(f"{apple['name']} - ISIN: {apple['isin']}")
        """
        instruments = self.get_all_instruments()
        for instrument in instruments:
            if instrument.get('ticker') == ticker:
                return instrument
        return None

    def clear_cache(self):
        """
        Clear the internal cache.

        Use this if you need to force a fresh fetch on the next request.
        """
        self._instruments_cache = None
        self._exchanges_cache = None
