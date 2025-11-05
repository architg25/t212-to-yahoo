"""
Account Data API endpoints.

Provides access to account information, cash balance, and metadata.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Trading212Client


class AccountAPI:
    """
    Account Data API.

    Access fundamental information about your trading account.
    """

    def __init__(self, client: 'Trading212Client'):
        """
        Initialize the Account API.

        Args:
            client: The main Trading212Client instance
        """
        self.client = client

    def get_cash(self) -> dict:
        """
        Get account cash balance.

        Rate Limit: 1 request per 2 seconds

        Returns:
            dict: Account cash data with fields:
                - free: Available cash for trading
                - total: Total account value
                - ppl: Unrealised profit and loss
                - result: Realised profit and loss
                - cash: Cash balance

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> client.account.get_cash()
            {
                'free': 10000.0,
                'total': 10000.0,
                'ppl': 0.0,
                'result': 10000.0,
                'cash': 10000.0
            }
        """
        return self.client.get('/equity/account/cash')

    def get_info(self) -> dict:
        """
        Get account information.

        Rate Limit: 1 request per 30 seconds

        Returns:
            dict: Account information with fields:
                - currencyCode: Account base currency (e.g., 'USD', 'GBP')
                - id: Account ID

        Raises:
            ValueError: If authentication fails
            RuntimeError: If the request fails

        Example:
            >>> client.account.get_info()
            {
                'currencyCode': 'USD',
                'id': 12345
            }
        """
        return self.client.get('/equity/account/info')
