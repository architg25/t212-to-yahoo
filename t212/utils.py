"""
Utility functions for the Trading212 API client.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Union


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
