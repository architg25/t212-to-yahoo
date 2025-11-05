"""
Portfolio API endpoints.

Provides access to portfolio positions and holdings.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import Trading212Client


class PortfolioAPI:
    """
    Portfolio API.

    View the current state of your portfolio, including open positions,
    quantity, average price, and current profit or loss.
    """

    def __init__(self, client: 'Trading212Client'):
        """
        Initialize the Portfolio API.

        Args:
            client: The main Trading212Client instance
        """
        self.client = client

    def get_all_positions(self) -> list:
        """
        Fetch all open positions.

        Rate Limit: 1 request per 5 seconds

        Returns:
            list: List of all open positions, each containing:
                - ticker: Instrument ticker (e.g., 'AAPL_US_EQ')
                - quantity: Number of shares
                - averagePrice: Average purchase price
                - currentPrice: Current market price
                - ppl: Profit and loss (unrealised)
                - fxPpl: Foreign exchange profit/loss (if applicable)
                - initialFillDate: Date of first purchase
                - frontend: Display ticker (e.g., 'AAPL')

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> client.portfolio.get_all_positions()
            [
                {
                    'ticker': 'AAPL_US_EQ',
                    'quantity': 10.0,
                    'averagePrice': 150.00,
                    'currentPrice': 155.00,
                    'ppl': 50.00,
                    'frontend': 'AAPL'
                }
            ]
        """
        return self.client.get('/equity/portfolio')

    def get_position(self, ticker: str) -> dict:
        """
        Fetch a specific position by ticker.

        Rate Limit: 1 request per 1 second

        Args:
            ticker: Instrument ticker (e.g., 'AAPL_US_EQ')

        Returns:
            dict: Position details with the same fields as get_all_positions

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails or position not found

        Example:
            >>> client.portfolio.get_position('AAPL_US_EQ')
            {
                'ticker': 'AAPL_US_EQ',
                'quantity': 10.0,
                'averagePrice': 150.00,
                'currentPrice': 155.00,
                'ppl': 50.00
            }
        """
        return self.client.get(f'/equity/portfolio/{ticker}')

    def search_position(self, ticker: str) -> dict:
        """
        Search for a specific position by ticker using POST.

        Rate Limit: 1 request per 1 second

        Args:
            ticker: Instrument ticker to search for

        Returns:
            dict: Position details

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> client.portfolio.search_position('AAPL')
            {
                'ticker': 'AAPL_US_EQ',
                'quantity': 10.0,
                ...
            }
        """
        return self.client.post('/equity/portfolio/ticker', {'ticker': ticker})
