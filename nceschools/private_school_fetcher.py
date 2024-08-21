# private_school_fetcher.py

"""
This module defines the `PrivateSchoolFetcher` class, which is responsible for fetching and extracting 
information about private schools from the National Center for Education Statistics (NCES) website. 
The class inherits from the `NCESFetcher` base class and provides methods specific to private school 
data retrieval and extraction.

Classes:
    PrivateSchoolFetcher: A class for retrieving and extracting private school information from the NCES website.

Methods:
    __init__(): Initializes the PrivateSchoolFetcher with the base URL for private schools.
    get_private_school_html(school_code): Retrieves the private school details based on the NCES school code.
    extract_school_details(html_content): Extracts private school details from the HTML content.
    extract_school_type(soup): Extracts the school type from the parsed HTML content.
    extract_physical_address(soup): Extracts the physical address from the parsed HTML content.
    extract_street_address(soup): Extracts the street address from the parsed HTML content.
    extract_city(soup): Extracts the city from the parsed HTML content.
    extract_state(soup): Extracts the state abbreviation from the parsed HTML content.
    extract_zip_body(soup): Extracts the zip code body (first 5 digits) from the parsed HTML content.
    extract_zip_suffix(soup): Extracts the zip code suffix (4 digits after the dash) from the parsed HTML content.
    extract_county(soup): Extracts the county from the parsed HTML content.
    extract_locale(soup): Extracts the locale from the parsed HTML content.
    extract_total_students(soup): Extracts the total number of students from the parsed HTML content.
    extract_classroom_teachers(soup): Extracts the number of classroom teachers from the parsed HTML content.
    extract_student_teacher_ratio(soup): Extracts the student-teacher ratio from the parsed HTML content.
    extract_grade_span(soup): Extracts the grade span from the parsed HTML content.
    extract_enrollment_by_race(soup): Extracts the enrollment by race/ethnicity from the parsed HTML content.

Usage:
    The `PrivateSchoolFetcher` class is used to interact with the NCES private school search tool, 
    allowing users to retrieve and extract detailed information about specific private schools using 
    their NCES school codes.

Examples:
    >>> fetcher = PrivateSchoolFetcher()
    >>> html_content = fetcher.get_private_school_html("12345678")
    >>> school_details = fetcher.extract_school_details(html_content)
    >>> print(school_details)
"""

import re
from bs4 import BeautifulSoup
from .nces_fetcher import NCESFetcher
from .nces_utils import NCESUtils

class PrivateSchoolFetcher(NCESFetcher):
    """
    Class for fetching and extracting information about private schools from the NCES website.
    """

    def __init__(self):
        """
        Initializes the PrivateSchoolFetcher with the base URL for private schools.
        """
        base_url = "https://nces.ed.gov/surveys/pss/privateschoolsearch/"
        super().__init__(base_url)

    def get_private_school_html(self, school_code):
        """
        Retrieves the private school details based on the NCES school code.

        Args:
            school_code (str): The NCES school code.

        Returns:
            str: The HTML content of the school details page.
        """
        query_params = {
            "Search": "1",
            "SchoolID": school_code,
            "NumOfStudentsRange": "more",
            "IncGrade": "-1",
            "LoGrade": "-1",
            "HiGrade": "-1",
            "ID": school_code
        }
        full_url = f"{self.base_url}school_detail.asp?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"

        return self.fetch_html_content(full_url)

    def extract_school_details(self, html_content):
        """
        Extracts private school details from the HTML content.

        Args:
            html_content (str): The HTML content of the school details page.

        Returns:
            dict: A dictionary with the extracted school details.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            school_type = self.extract_school_type(soup)
            physical_address = self.extract_physical_address(soup)
            county = self.extract_county(soup)
            locale = self.extract_locale(soup)
            total_students = self.extract_total_students(soup)
            classroom_teachers = self.extract_classroom_teachers(soup)
            student_teacher_ratio = self.extract_student_teacher_ratio(soup)
            grade_span = self.extract_grade_span(soup)
            enrollment_by_race = self.extract_enrollment_by_race(soup)

            return {
                'Type': school_type,
                'Physical Address': physical_address,
                'County': county,
                'Locale': locale,
                'Total Students': total_students,
                'Classroom Teachers': classroom_teachers,
                'Student/Teacher Ratio': student_teacher_ratio,
                'Grade Span': grade_span,
                **enrollment_by_race
            }

        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

    def extract_school_type(self, soup):
        """
        Extracts the school type from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The type of the school or None if not found.
        """
        type_element = soup.find('th', string="Type:")
        if type_element:
            next_td = type_element.find_next('td')
            if next_td:
                return next_td.get_text(strip=True)
        return None

    def extract_physical_address(self, soup):
        """
        Extracts the physical address from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The physical address or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            address_lines = []
            for element in address_tag.next_siblings:
                if element.name == 'br':
                    continue
                elif element.name and element.name != 'font':
                    break
                text = element.strip() if isinstance(element, str) else element.get_text(strip=True)
                if text:
                    address_lines.append(text)
            return " ".join(address_lines).replace('\xa0', ' ')
        return None

    def extract_street_address(self, soup):
        """
        Extracts the street address from the parsed HTML content for private schools.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The street address or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            address_element = str(address_tag.next_sibling.next_sibling)
            street_address = address_element.split('<br />')[0].strip()
            return street_address
        return None

    def extract_city(self, soup):
        """
        Extracts the city from the parsed HTML content for private schools.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The city or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            address_content = str(address_tag.next_sibling.next_sibling.next_sibling.next_sibling)
            print(address_content)
            city = address_content.split(',')[0].strip()
            return city
        return None

    def extract_state(self, soup):
        """
        Extracts the state from the parsed HTML content for private schools.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The state abbreviation or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            # Get the full address content after the second <br />
            address_content = str(address_tag.next_sibling.next_sibling.next_sibling.next_sibling)
            # Use regex to find the two-letter state abbreviation
            match = re.search(r',\s([A-Z]{2})\s', address_content)
            if match:
                return match.group(1)
        return None


    def extract_zip_body(self, soup):
        """
        Extracts the zip code body (first 5 digits) from the parsed HTML content for private schools.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The zip code body or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            # Get the full address content after the second <br />
            address_content = str(address_tag.next_sibling.next_sibling.next_sibling.next_sibling)
            # Use regex to find the first five digits of the zip code
            match = re.search(r'\s(\d{5})', address_content)
            if match:
                return match.group(1)
        return None

    def extract_zip_suffix(self, soup):
        """
        Extracts the zip code suffix (4 digits after the dash) from the parsed HTML content for private schools.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The zip code suffix or None if not found.
        """
        address_tag = soup.find('strong', string="Physical Address:")
        if address_tag:
            # Get the full address content after the second <br />
            address_content = str(address_tag.next_sibling.next_sibling.next_sibling.next_sibling)
            # Use regex to find the four digits after the dash
            match = re.search(r'-(\d{4})', address_content)
            if match:
                return match.group(1)
        return None

    def extract_county(self, soup):
        """
        Extracts the county from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The county or None if not found.
        """
        return NCESUtils.get_text_after_label(soup, "County:")

    def extract_locale(self, soup):
        """
        Extracts the locale from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The locale or None if not found.
        """
        locale_element = soup.find(string="Locale/Code:")
        if locale_element:
            next_td = locale_element.find_next('td')
            if next_td:
                return next_td.text.strip()
        return None

    def extract_total_students(self, soup):
        """
        Extracts the total number of students from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            int: The total number of students or None if not found.
        """
        return NCESUtils.get_int_after_label(soup, "Total Students:")

    def extract_classroom_teachers(self, soup):
        """
        Extracts the number of classroom teachers from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            float: The number of classroom teachers or None if not found.
        """
        return NCESUtils.get_float_after_label(soup, "Classroom Teachers (FTE):")

    def extract_student_teacher_ratio(self, soup):
        """
        Extracts the student-teacher ratio from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            float: The student-teacher ratio or None if not found.
        """
        return NCESUtils.get_float_after_label(soup, "Student/Teacher Ratio:")

    def extract_grade_span(self, soup):
        """
        Extracts the grade span from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The grade span or None if not found.
        """
        grade_span_tag = soup.find('strong', string="Grade Span:")
        if grade_span_tag:
            grade_span_text = grade_span_tag.find_next_sibling('font')
            if grade_span_text:
                match = re.search(r"\(grades (.*?)\)", grade_span_text.get_text(strip=True))
                if match:
                    return match.group(1).replace(" ", "")
        return None

    def extract_enrollment_by_race(self, soup):
        """
        Extracts the enrollment by race/ethnicity from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            dict: A dictionary with the enrollment by race/ethnicity.
        """
        race_table = soup.find(string="Enrollment by Race/Ethnicity:")
        if race_table:
            race_table = race_table.find_next('table')
            races = race_table.find_all('td', bgcolor='#B8EEA8') if race_table else []
            enrollment_by_race = [NCESUtils.get_int(race.text.strip()) for race in races[:7]] if races else [None] * 7
        else:
            enrollment_by_race = [None] * 7

        return {
            'American Indian/Alaska Native': enrollment_by_race[0],
            'Asian': enrollment_by_race[1],
            'Black': enrollment_by_race[2],
            'Hispanic': enrollment_by_race[3],
            'White': enrollment_by_race[4],
            'Native Hawaiian/Pacific Islander': enrollment_by_race[5],
            'Two or More Races': enrollment_by_race[6]
        }

