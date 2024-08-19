# mces_utils.py

"""
This module defines the `NCESUtils` class, which provides utility methods for common operations 
when handling HTML content from the National Center for Education Statistics (NCES) websites. 
These static methods facilitate extracting integers, floats, and text from specific labels within 
HTML documents.

Classes:
    NCESUtils: A utility class offering static methods to extract data from HTML content based on labels.

Methods:
    get_int(text): Extracts the first integer found in a given string.
    get_int_after_label(soup, label): Finds and returns an integer located after a specified label in an HTML document.
    get_float_after_label(soup, label): Finds and returns a float located after a specified label in an HTML document.
    get_text_after_label(soup, label): Finds and returns text located after a specified label in an HTML document.

Usage:
    The `NCESUtils` class is designed to be used with BeautifulSoup objects representing parsed HTML content.
    These methods can be used to locate and extract specific data points from NCES HTML pages.

Examples:
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> student_count = NCESUtils.get_int_after_label(soup, "Total Students:")
    >>> student_teacher_ratio = NCESUtils.get_float_after_label(soup, "Student/Teacher Ratio:")
    >>> county_name = NCESUtils.get_text_after_label(soup, "County:")
"""

import re

class NCESUtils:
    """Utility class for common NCES operations."""

    @staticmethod
    def get_int(text):
        """Extract the first integer from a string."""
        result = re.sub(r'\D', '', text)
        return int(result) if result else None

    @staticmethod
    def get_int_after_label(soup, label):
        """Find an integer after a specific label in the HTML."""
        label_element = soup.find(string=label)
        if label_element:
            parent_td = label_element.find_parent('td')
            if parent_td:
                next_td = parent_td.find_next_siblings('td')
                for td in next_td:
                    result = NCESUtils.get_int(td.get_text(strip=True))
                    if result is not None:
                        return result
        return None

    @staticmethod
    def get_float_after_label(soup, label):
        """Find a float after a specific label in the HTML using regex to handle leading spaces."""
        label_regex = re.compile(r'\s*' + re.escape(label))
        label_element = soup.find(string=label_regex)
        if label_element:
            parent_td = label_element.find_parent('td')
            if parent_td:
                next_td = parent_td.find_next_siblings('td')
                for td in next_td:
                    try:
                        return float(td.get_text(strip=True))
                    except ValueError:
                        continue
        return None

    @staticmethod
    def get_text_after_label(soup, label):
        label_element = soup.find(string=label)
        if label_element:
            parent_td = label_element.find_parent(['td', 'tr'])
            if parent_td:
                all_text = parent_td.stripped_strings
                for text in all_text:
                    if label in text:
                        return next(all_text, None)
        return None
