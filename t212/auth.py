"""
Authentication module for Trading212 API.

Handles HTTP Basic Authentication using API key and secret.
"""

import base64


class BasicAuthHandler:
    """
    Handles HTTP Basic Authentication for Trading212 API.

    The Trading212 API uses Basic Auth where:
    - API Key is the username
    - API Secret is the password
    """

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("Both API key and secret are required")

        self.api_key = api_key
        self.api_secret = api_secret
        self._auth_header = self._build_auth_header()

    def _build_auth_header(self) -> str:
        """
        Build the Authorization header value.

        Returns:
            str: Authorization header value in format "Basic <base64_encoded>"
        """
        credentials_string = f"{self.api_key}:{self.api_secret}"
        encoded_credentials = base64.b64encode(
            credentials_string.encode('utf-8')
        ).decode('utf-8')

        return f"Basic {encoded_credentials}"

    def get_auth_header(self) -> str:
        """
        Get the pre-built Authorization header value.

        Returns:
            str: Authorization header value
        """
        return self._auth_header

    def get_headers(self) -> dict:
        """
        Get HTTP headers including authorization.

        Returns:
            dict: Headers dictionary ready for requests
        """
        return {
            'Authorization': self._auth_header,
            'Content-Type': 'application/json'
        }
