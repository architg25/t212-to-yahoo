"""
Base Trading212 API Client.

Handles HTTP communication and provides access to API endpoints.
"""

import requests
from typing import Optional

from .auth import BasicAuthHandler
from .account import AccountAPI
from .portfolio import PortfolioAPI
from .instruments import InstrumentsAPI


class Trading212Client:
    """
    Main client for interacting with the Trading212 API.

    Handles authentication and provides access to different API sections.
    """

    BASE_URLS = {
        'live': 'https://live.trading212.com/api/v0',
        'demo': 'https://demo.trading212.com/api/v0'
    }

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        environment: str = 'demo',
        timeout: int = 30
    ):
        """
        Initialize the Trading212 client.

        Args:
            api_key: Your Trading212 API key
            api_secret: Your Trading212 API secret
            environment: 'live' or 'demo' (default: 'demo')
            timeout: Request timeout in seconds (default: 30)

        Raises:
            ValueError: If credentials are invalid or environment is not 'live' or 'demo'
        """
        if environment not in self.BASE_URLS:
            raise ValueError(
                f"Invalid environment. Must be 'live' or 'demo', got: {environment}"
            )

        self.environment = environment
        self.base_url = self.BASE_URLS[environment]
        self.timeout = timeout

        self.auth_handler = BasicAuthHandler(api_key, api_secret)

        self.session = requests.Session()
        self.session.headers.update(self.auth_handler.get_headers())

        self.account = AccountAPI(self)
        self.portfolio = PortfolioAPI(self)
        self.instruments = InstrumentsAPI(self)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None
    ) -> requests.Response:
        """
        Make an HTTP request to the Trading212 API.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path (e.g., '/equity/account/cash')
            params: Optional query parameters
            json_data: Optional JSON body data

        Returns:
            requests.Response: The API response

        Raises:
            requests.HTTPError: If the request fails
            requests.RequestException: For network-related errors
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    "Authentication failed. Check your API key and secret."
                ) from e
            elif e.response.status_code == 403:
                raise ValueError(
                    "Access forbidden. Verify API key permissions."
                ) from e
            elif e.response.status_code == 429:
                raise RuntimeError(
                    "Rate limit exceeded. Check response headers for reset time."
                ) from e
            else:
                raise

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}") from e

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            dict: Parsed JSON response
        """
        response = self.request('GET', endpoint, params=params)
        return response.json()

    def post(self, endpoint: str, json_data: dict) -> dict:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint path
            json_data: JSON body data

        Returns:
            dict: Parsed JSON response
        """
        response = self.request('POST', endpoint, json_data=json_data)
        return response.json()

    def delete(self, endpoint: str) -> dict:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            dict: Parsed JSON response
        """
        response = self.request('DELETE', endpoint)
        return response.json()
