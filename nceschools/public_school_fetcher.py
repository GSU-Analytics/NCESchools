# public_school_fetcher.py

"""
This module defines the `PublicSchoolFetcher` class, which is responsible for fetching and extracting 
information about public schools from the National Center for Education Statistics (NCES) website. 
The class inherits from the `NCESFetcher` base class and provides methods specific to public school 
data retrieval and extraction.

Classes:
    PublicSchoolFetcher: A class for retrieving and extracting public school information from the NCES website.

Methods:
    __init__(): Initializes the PublicSchoolFetcher with the base URL for public schools.
    get_public_school_html(school_code): Retrieves the public school details based on the NCES school code.
    extract_school_details(html_content): Extracts public school details from the HTML content.
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
    extract_enrollment_by_gender(soup): Extracts the enrollment by gender from the parsed HTML content.
    extract_lunch_eligibility(soup): Extracts the lunch eligibility data from the parsed HTML content.

Usage:
    The `PublicSchoolFetcher` class is used to interact with the NCES public school search tool, 
    allowing users to retrieve and extract detailed information about specific public schools using 
    their NCES school codes.

Examples:
    >>> fetcher = PublicSchoolFetcher()
    >>> html_content = fetcher.get_public_school_html("12345678")
    >>> school_details = fetcher.extract_school_details(html_content)
    >>> print(school_details)
"""


import re
from bs4 import BeautifulSoup
from .nces_fetcher import NCESFetcher
from .nces_utils import NCESUtils

class PublicSchoolFetcher(NCESFetcher):
    """
    Class for fetching and extracting information about public schools from the NCES website.
    """

    def __init__(self):
        """
        Initializes the PublicSchoolFetcher with the base URL for public schools.
        """
        base_url = "https://nces.ed.gov/ccd/schoolsearch/"
        super().__init__(base_url)

    def get_public_school_html(self, school_code):
        """
        Retrieves the public school details based on the NCES school code.

        Args:
            school_code (str): The NCES school code.

        Returns:
            str: The HTML content of the school details page.
        """
        school_code = school_code.zfill(12)
        query_params = {
            "Search": "1",
            "SchoolID": school_code,
            "SchoolType": "1",
            "SpecificSchlTypes": "all",
            "IncGrade": "-1",
            "LoGrade": "-1",
            "HiGrade": "-1",
            "ID": school_code
        }
        full_url = f"{self.base_url}school_detail.asp?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"

        return self.fetch_html_content(full_url)

    def extract_school_details(self, html_content):
        """
        Extracts public school details from the HTML content.

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
            enrollment_by_gender = self.extract_enrollment_by_gender(soup)
            lunch_eligibility = self.extract_lunch_eligibility(soup)

            return {
                'Type': school_type,
                'Physical Address': physical_address,
                'County': county,
                'Locale': locale,
                'Total Students': total_students,
                'Classroom Teachers': classroom_teachers,
                'Student/Teacher Ratio': student_teacher_ratio,
                'Grade Span': grade_span,
                **enrollment_by_race,
                **enrollment_by_gender,
                **lunch_eligibility
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
        type_label = soup.find(string=re.compile("Type:"))
        if type_label:
            type_element = type_label.find_next('font', size="3")
            if type_element:
                return type_element.text.strip()
        return None

    def extract_physical_address(self, soup):
        """
        Extracts the physical address from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The physical address or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_lines = address_element.contents
                address = " ".join([line.strip() for line in address_lines if isinstance(line, str)])
                return address.replace('&nbsp;', ' ').replace('\xa0', ' ')
        return None
    
    def extract_street_address(self, soup):
        """
        Extracts the street address from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The street address or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_string = str(address_element)
                start = 'Navigator">'
                end = '<br/>'
                street_address = address_string.split(start)[-1].split(end)[0].strip()
                return street_address
        return None

    def extract_city(self, soup):
        """
        Extracts the city name from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The city name or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_string = str(address_element)

                # Use regex to find the city name, which appears before the comma
                match = re.search(r'>([^<]+),\s[A-Z]{2}\s\d{5}', address_string)
                if match:
                    city = match.group(1).strip()
                    return city
        return None

    def extract_state(self, soup):
        """
        Extracts the state abbreviation from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The state abbreviation or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_string = str(address_element)
                
                # Use regex to find the two-letter state abbreviation
                match = re.search(r',\s([A-Z]{2})\s\d{5}', address_string)
                if match:
                    state_abbr = match.group(1)
                    return state_abbr
        return None

    def extract_zip_body(self, soup):
        """
        Extracts the 5-digit ZIP code body from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The 5-digit ZIP code body or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_string = str(address_element)
                
                # Use regex to find the 5-digit ZIP code body
                match = re.search(r',\s[A-Z]{2}\s(\d{5})(?:-\d{4})?</a>', address_string)
                if match:
                    zip_body = match.group(1)
                    return zip_body
        return None

    def extract_zip_suffix(self, soup):
        """
        Extracts the ZIP code suffix (the four digits after the dash in the ZIP+4 code)
        from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            str: The ZIP code suffix or None if not found.
        """
        address_tag = soup.find('font', string="Physical Address:")
        if address_tag:
            address_element = address_tag.find_next('font', size='3').find('a')
            if address_element:
                address_string = str(address_element)
                
                # Use regex to find the ZIP+4 suffix
                match = re.search(r'(\d{5})-(\d{4})</a>', address_string)
                if match:
                    zip_suffix = match.group(2)
                    return zip_suffix
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
        for strong_tag in soup.find_all('strong'):
            if "Locale:" in strong_tag.text:
                return strong_tag.next_sibling.strip()
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
        grade_span_tag = soup.find(string=re.compile(r"Grade Span:"))
        if grade_span_tag:
            grade_span_text = grade_span_tag.find_next(string=re.compile(r"\(grades.*\)"))
            if grade_span_text:
                match = re.search(r"\(grades (.*?)\)", grade_span_text)
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
            'American Native': enrollment_by_race[0],
            'Asian': enrollment_by_race[1],
            'Black': enrollment_by_race[2],
            'Hispanic': enrollment_by_race[3],
            'Pacific Islander': enrollment_by_race[4],
            'White': enrollment_by_race[5],
            'Multiple Races': enrollment_by_race[6]
        }

    def extract_enrollment_by_gender(self, soup):
        """
        Extracts the enrollment by gender from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            dict: A dictionary with the enrollment by gender.
        """
        gender_table = soup.find(string="Enrollment by Gender:")
        if gender_table:
            gender_table = gender_table.find_next('table')
            genders = gender_table.find_all('td', bgcolor='#F5F196') if gender_table else []
            enrollment_by_gender = [NCESUtils.get_int(gender.text.strip()) for gender in genders[:2]] if genders else [None, None]
        else:
            enrollment_by_gender = [None, None]

        return {
            'Male Enrollment': enrollment_by_gender[0],
            'Female Enrollment': enrollment_by_gender[1]
        }

    def extract_lunch_eligibility(self, soup):
        """
        Extracts the lunch eligibility data from the parsed HTML content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            dict: A dictionary with the lunch eligibility data.
        """
        lunch_eligibility_table = soup.find(string="Free lunch eligible")
        if lunch_eligibility_table:
            parent_row = lunch_eligibility_table.find_parent('tr')
            if parent_row:
                columns = parent_row.find_all('td')
                if len(columns) >= 3:
                    free_lunch_eligible = NCESUtils.get_int(columns[0].find('font').contents[-1].strip())
                    reduced_price_lunch_eligible = NCESUtils.get_int(columns[1].find('font').contents[-1].strip())
                    total_lunch_eligible = NCESUtils.get_int(columns[2].find('font').contents[-1].strip())
                    return {
                        'Free lunch eligible': free_lunch_eligible,
                        'Reduced lunch eligible': reduced_price_lunch_eligible,
                        'Free/reduced total eligible': total_lunch_eligible
                    }
        return {
            'Free lunch eligible': None,
            'Reduced-price lunch eligible': None,
            'Total (Free and reduced lunch eligible)': None
        }
