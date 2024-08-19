# nces_fetcher.py

"""
This module defines the `NCESFetcher` class, a base class for fetching and handling HTML content 
from the National Center for Education Statistics (NCES) websites. It provides methods for 
retrieving HTML content from given URLs and saving that content to local files.

Classes:
    NCESFetcher: A base class for fetching and handling HTML content from NCES websites.

Usage:
    The `NCESFetcher` class can be used as a parent class for specific fetchers that need to 
    interact with different sections of the NCES website. It provides methods to fetch HTML 
    content from a URL and save it to a specified directory.

Examples:
    >>> fetcher = NCESFetcher(base_url="https://nces.ed.gov/ccd/schoolsearch/")
    >>> html_content = fetcher.fetch_html_content(full_url="https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID=010001000011")
    >>> fetcher.save_html(html_content, filename="school.html")
"""

import os
import requests

class NCESFetcher:
    """
    Base class for fetching and handling HTML content from the NCES websites.
    """

    def __init__(self, base_url):
        """
        Initializes the NCESFetcher with the base URL.

        Args:
            base_url (str): The base URL for the NCES search.
        """
        self.base_url = base_url

    def fetch_html_content(self, full_url):
        """
        Fetches the HTML content from a given URL.

        Args:
            full_url (str): The full URL to fetch the HTML content from.

        Returns:
            str: The HTML content of the page.

        Raises:
            Exception: If the request to the URL fails.
        """
        response = requests.get(full_url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. Got response: {response.status_code}")
        return response.text

    def save_html(self, html_content, filename, save_directory="./html"):
        """
        Saves HTML content to a specified directory with a given filename.

        Args:
            html_content (str): The HTML content to save.
            filename (str): The name of the file to save the content as.
            save_directory (str): The directory to save the file in.

        Returns:
            str: The path to the saved file.
        """
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML content saved to {file_path}")
        return file_path