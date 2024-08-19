# school_searcher.py

"""
This module defines the `SchoolSearcher` class, which is responsible for searching NCES school information 
for both public and private schools. The class provides methods to fetch HTML content, save it, and extract 
the NCES School ID based on search criteria such as school name, city, state, and zipcode.

Classes:
    SchoolSearcher: A class for searching NCES school information for both public and private schools.

Methods:
    __init__(school_type='public'): Initializes the SchoolSearcher with the specified school type.
    fetch_html_content(full_url): Fetches the HTML content from a given URL.
    save_html(html_content, filename, save_directory="./html"): Saves HTML content to a specified directory with a given filename.
    extract_nces_school_id(soup): Extracts the NCES School ID from the parsed HTML content.
    get_school_search_html(school_name): Constructs the search URL and fetches HTML content for a given school name.
    find_school_url_by_location(html_content, city=None, zip_code=None, state=None): Finds the school URL based on location criteria such as city, zip code, and state.
    get_nces_id(school_name, city=None, state=None, zip_code=None): Returns the NCES ID for a school based on the provided school name, city, state, and/or zipcode.

Usage:
    The `SchoolSearcher` class is used to interact with the NCES school search tools, allowing users to 
    search for both public and private schools and retrieve their NCES School IDs based on various search 
    criteria.

Examples:
    >>> searcher = SchoolSearcher(school_type='public')
    >>> nces_id = searcher.get_nces_id("Shiloh High School", city="Snellville", state="GA", zip_code="30039")
    >>> print(nces_id)
"""

import os
import requests
from bs4 import BeautifulSoup

class SchoolSearcher:
    """
    Class for searching NCES school information for both public and private schools.
    """

    def __init__(self, school_type='public'):
        """
        Initializes the SchoolSearcher with the specified school type.

        Args:
            school_type (str): The type of school to search ('public' or 'private').
        """
        self.school_type = school_type

    def fetch_html_content(self, full_url):
        """Fetch the HTML content from a given URL."""
        response = requests.get(full_url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data. Got response: {response.status_code}")
        return response.text

    def save_html(self, html_content, filename, save_directory="./html"):
        """Save HTML content to a specified directory with a given filename."""
        os.makedirs(save_directory, exist_ok=True)
        file_path = os.path.join(save_directory, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML content saved to {file_path}")
        return file_path

    def extract_nces_school_id(self, soup):
        """Extract the NCES School ID from the parsed HTML content."""
        if self.school_type == 'public':
            nces_id_label = soup.find('font', string="NCES School ID:")
            if nces_id_label:
                nces_id_element = nces_id_label.find_next('font', size="3")
                if nces_id_element:
                    return nces_id_element.text.strip()
        elif self.school_type == 'private':
            nces_id_label = soup.find('strong', string=lambda s: s and "NCES School ID:" in s)
            if nces_id_label:
                nces_id_element = nces_id_label.find_next('br').next_sibling
                if nces_id_element:
                    return nces_id_element.strip()
        return None

    def get_school_search_html(self, school_name):
        """Construct the search URL and fetch HTML content for a given school name."""
        school_name = school_name.replace(" ", "+")
        
        if self.school_type == 'public':
            base_url = "https://nces.ed.gov/ccd/schoolsearch/school_list.asp"
            query_params = {
                "Search": "1",
                "InstName": school_name,
                "SchoolID": "",
                "Address": "",
                "City": "",
                "State": "",
                "Zip": "",
                "Miles": "",
                "County": "",
                "PhoneAreaCode": "",
                "Phone": "",
                "DistrictName": "",
                "DistrictID": "",
                "SpecificSchlTypes": "all",
                "IncGrade": "-1",
                "LoGrade": "-1",
                "HiGrade": "-1"
            }
            school_type_params = "&".join([f"SchoolType={i}" for i in range(1, 5)])
            full_url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}&{school_type_params}"
        
        elif self.school_type == 'private':
            base_url = "https://nces.ed.gov/surveys/pss/privateschoolsearch/school_list.asp"
            query_params = {
                "Search": "1",
                "SchoolName": school_name,
                "SchoolID": "",
                "Address": "",
                "City": "",
                "State": "",
                "Zip": "",
                "Miles": "",
                "County": "",
                "PhoneAreaCode": "",
                "Phone": "",
                "Religion": "",
                "Association": "",
                "SchoolType": "",
                "Coed": "",
                "NumOfStudents": "",
                "NumOfStudentsRange": "more",
                "IncGrade": "-1",
                "LoGrade": "-1",
                "HiGrade": "-1"
            }
            full_url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"
        
        return self.fetch_html_content(full_url)

    def find_school_url_by_location(self, html_content, city=None, zip_code=None, state=None):
        """Find the school URL based on location criteria such as city, zip code, and state."""
        if self.school_type == 'public':
            base_url = "https://nces.ed.gov/ccd/schoolsearch/"
            school_entries_selector = 'tr'
            address_index = 1
        elif self.school_type == 'private':
            base_url = "https://nces.ed.gov/surveys/pss/privateschoolsearch/"
            school_entries_selector = 'tr[style*="background-color: #EDFFE8;"]'
            address_index = 1

        soup = BeautifulSoup(html_content, 'html.parser')
        school_entries = soup.select(school_entries_selector)

        best_match = None
        best_priority = float('inf')

        for entry in school_entries:
            school_info = entry.find('a', href=True)
            if school_info:
                # Ensure the entry has enough <td> elements before accessing
                tds = entry.find_all('td')
                if len(tds) <= address_index:
                    continue
                
                school_link = school_info['href']
                school_address = tds[address_index].text.strip()
                
                address_parts = school_address.split(',')
                
                if len(address_parts) < 2:
                    continue
                
                school_city = address_parts[-2].strip() if len(address_parts) > 1 else ""
                state_zip_parts = address_parts[-1].strip().split() if len(address_parts) > 0 else []
                school_state = state_zip_parts[-2] if len(state_zip_parts) > 1 else ""
                school_zip = state_zip_parts[-1] if len(state_zip_parts) > 0 else ""
                
                if city and zip_code and state:
                    if school_city.lower() == city.lower() and school_zip == zip_code and school_state.upper() == state.upper():
                        return f"{base_url}{school_link}"
                elif state and city:
                    if school_city.lower() == city.lower() and school_state.upper() == state.upper():
                        if best_priority > 2:
                            best_match = f"{base_url}{school_link}"
                            best_priority = 2
                elif zip_code:
                    if school_zip == zip_code:
                        if best_priority > 3:
                            best_match = f"{base_url}{school_link}"
                            best_priority = 3
                elif city:
                    if school_city.lower() == city.lower():
                        if best_priority > 4:
                            best_match = f"{base_url}{school_link}"
                            best_priority = 4
                elif state:
                    if school_state.upper() == state.upper():
                        if best_priority > 5:
                            best_match = f"{base_url}{school_link}"
                            best_priority = 5
        
        next_page_link = soup.find('a', string="Next >>")
        if next_page_link and best_match is None:
            next_page_url = base_url + next_page_link['href']
            next_page_html = self.fetch_html_content(next_page_url)
            return self.find_school_url_by_location(next_page_html, city, zip_code, state)
        
        return best_match

    def get_nces_id(self, school_name, city=None, state=None, zip_code=None):
        """
        Returns the NCES ID for a school based on the provided school name, city, state, and/or zipcode.

        Args:
            school_name (str): The name of the school.
            city (str, optional): The city where the school is located.
            state (str, optional): The state where the school is located.
            zip_code (str, optional): The zipcode of the school's location.

        Returns:
            str: The NCES ID of the school if found, otherwise None.
        """
        # First, search in public school data
        search_html_content = self.get_school_search_html(school_name)
        school_url = self.find_school_url_by_location(search_html_content, city=city, state=state, zip_code=zip_code)

        if school_url:
            school_html_content = self.fetch_html_content(school_url)
            soup = BeautifulSoup(school_html_content, 'html.parser')
            nces_code = self.extract_nces_school_id(soup)
            if nces_code:
                return nces_code

        # If not found, switch to private school search if applicable
        if self.school_type == 'public':
            self.school_type = 'private'
            return self.get_nces_id(school_name, city=city, state=state, zip_code=zip_code)

        return None