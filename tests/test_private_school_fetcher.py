# test_private_school_fetcher.py

import pytest
from nceschools.private_school_fetcher import PrivateSchoolFetcher

def test_extract_school_type_private(fuqua_school_soup, grace_christian_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_school_type(fuqua_school_soup) == "Regular elementary or secondary", f"Expected 'Regular elementary or secondary', got '{fetcher.extract_school_type(fuqua_school_soup)}'"
    assert fetcher.extract_school_type(grace_christian_school_soup) == "Regular elementary or secondary", f"Expected 'Regular elementary or secondary', got '{fetcher.extract_school_type(grace_christian_school_soup)}'"

def test_extract_physical_address_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_physical_address(grace_christian_school_soup) == "600 Lind St Mankato, MN 56001", f"Expected '600 Lind St Mankato, MN 56001', got '{fetcher.extract_physical_address(grace_christian_school_soup)}'"
    assert fetcher.extract_physical_address(fuqua_school_soup) == "Po Box 328 Farmville, VA 23901-0328", f"Expected 'Po Box 328 Farmville, VA 23901-0328', got '{fetcher.extract_physical_address(fuqua_school_soup)}'"

def test_extract_street_address_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_street_address(grace_christian_school_soup) == "600 Lind St", f"Expected '600 Lind St', got '{fetcher.extract_street_address(grace_christian_school_soup)}'"
    assert fetcher.extract_street_address(fuqua_school_soup) == "Po Box 328", f"Expected 'Po Box 328', got '{fetcher.extract_street_address(fuqua_school_soup)}'"

def test_extract_city_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_city(grace_christian_school_soup) == "Mankato", f"Expected 'Mankato', got '{fetcher.extract_city(grace_christian_school_soup)}'"
    assert fetcher.extract_city(fuqua_school_soup) == "Farmville", f"Expected 'Farmville', got '{fetcher.extract_city(fuqua_school_soup)}'"

def test_extract_state_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_state(grace_christian_school_soup) == "MN", f"Expected 'MN', got '{fetcher.extract_state(grace_christian_school_soup)}'"
    assert fetcher.extract_state(fuqua_school_soup) == "VA", f"Expected 'VA', got '{fetcher.extract_state(fuqua_school_soup)}'"

def test_extract_zip_body_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_zip_body(grace_christian_school_soup) == "56001", f"Expected '56001', got '{fetcher.extract_zip_body(grace_christian_school_soup)}'"
    assert fetcher.extract_zip_body(fuqua_school_soup) == "23901", f"Expected '23901', got '{fetcher.extract_zip_body(fuqua_school_soup)}'"

def test_extract_zip_suffix_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_zip_suffix(grace_christian_school_soup) is None, f"Expected None, got '{fetcher.extract_zip_suffix(grace_christian_school_soup)}'"
    assert fetcher.extract_zip_suffix(fuqua_school_soup) == "0328", f"Expected '0328', got '{fetcher.extract_zip_suffix(fuqua_school_soup)}'"

def test_extract_county_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_county(grace_christian_school_soup) == "Blue Earth", f"Expected 'Blue Earth', got '{fetcher.extract_county(grace_christian_school_soup)}'"
    assert fetcher.extract_county(fuqua_school_soup) == "Prince Edward", f"Expected 'Prince Edward', got '{fetcher.extract_county(fuqua_school_soup)}'"

def test_extract_locale_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_locale(grace_christian_school_soup) == "Small city / 13", f"Expected 'Small city / 13', got '{fetcher.extract_locale(grace_christian_school_soup)}'"
    assert fetcher.extract_locale(fuqua_school_soup) == "Remote town / 33", f"Expected 'Remote town / 33', got '{fetcher.extract_locale(fuqua_school_soup)}'"

def test_extract_total_students_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_total_students(grace_christian_school_soup) == 50, f"Expected 50, got {fetcher.extract_total_students(grace_christian_school_soup)}"
    assert fetcher.extract_total_students(fuqua_school_soup) == 298, f"Expected 298, got {fetcher.extract_total_students(fuqua_school_soup)}"

def test_extract_classroom_teachers_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_classroom_teachers(grace_christian_school_soup) == 6.3, f"Expected 6.3, got {fetcher.extract_classroom_teachers(grace_christian_school_soup)}"
    assert fetcher.extract_classroom_teachers(fuqua_school_soup) == 28.1, f"Expected 28.1, got {fetcher.extract_classroom_teachers(fuqua_school_soup)}"

def test_extract_student_teacher_ratio_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_student_teacher_ratio(grace_christian_school_soup) == 7.8, f"Expected 7.8, got {fetcher.extract_student_teacher_ratio(grace_christian_school_soup)}"
    assert fetcher.extract_student_teacher_ratio(fuqua_school_soup) == 9.3, f"Expected 9.3, got {fetcher.extract_student_teacher_ratio(fuqua_school_soup)}"

def test_extract_grade_span_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    assert fetcher.extract_grade_span(grace_christian_school_soup) == "PK-12", f"Expected 'PK-12', got '{fetcher.extract_grade_span(grace_christian_school_soup)}'"
    assert fetcher.extract_grade_span(fuqua_school_soup) == "PK-12", f"Expected 'PK-12', got '{fetcher.extract_grade_span(fuqua_school_soup)}'"

def test_extract_enrollment_by_race_private(grace_christian_school_soup, fuqua_school_soup):
    fetcher = PrivateSchoolFetcher()
    grace_christian_expected = {
        'American Indian/Alaska Native': 0,
        'Asian': 2,
        'Black': 4,
        'Hispanic': 3,
        'White': 40,
        'Native Hawaiian/Pacific Islander': 0,
        'Two or More Races': 0
    }
    fuqua_expected = {
        'American Indian/Alaska Native': 4,
        'Asian': 8,
        'Black': 17,
        'Hispanic': 5,
        'White': 221,
        'Native Hawaiian/Pacific Islander': 1,
        'Two or More Races': 4
    }
    assert fetcher.extract_enrollment_by_race(grace_christian_school_soup) == grace_christian_expected, f"Expected {grace_christian_expected}, got {fetcher.extract_enrollment_by_race(grace_christian_school_soup)}"
    assert fetcher.extract_enrollment_by_race(fuqua_school_soup) == fuqua_expected, f"Expected {fuqua_expected}, got {fetcher.extract_enrollment_by_race(fuqua_school_soup)}"
