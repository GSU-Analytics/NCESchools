import pytest
from bs4 import BeautifulSoup
from nceschools.public_school_fetcher import PublicSchoolFetcher

def test_extract_school_type_public(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_school_type(anniston_soup) == "Regular school", f"Expected 'Regular school', got '{public_school_fetcher.extract_school_type(anniston_soup)}'"
    assert public_school_fetcher.extract_school_type(shiloh_soup) == "Regular school", f"Expected 'Regular school', got '{public_school_fetcher.extract_school_type(shiloh_soup)}'"
    assert public_school_fetcher.extract_school_type(south_haven_soup) == "Regular school", f"Expected 'Regular school', got '{public_school_fetcher.extract_school_type(south_haven_soup)}'"

def test_extract_physical_address_public(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_physical_address(anniston_soup) == "1301 Woodstock Ave Anniston, AL 36207", f"Expected '1301 Woodstock Ave Anniston, AL 36207', got '{public_school_fetcher.extract_physical_address(anniston_soup)}'"
    assert public_school_fetcher.extract_physical_address(shiloh_soup) == "4210 Shiloh Rd Snellville, GA 30039", f"Expected '4210 Shiloh Rd Snellville, GA 30039', got '{public_school_fetcher.extract_physical_address(shiloh_soup)}'"
    assert public_school_fetcher.extract_physical_address(south_haven_soup) == "600 ELKENBURG ST SOUTH HAVEN, MI 49090-1980", f"Expected '600 ELKENBURG ST SOUTH HAVEN, MI 49090-1980', got '{public_school_fetcher.extract_physical_address(south_haven_soup)}'"

def test_extract_county(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_county(anniston_soup) == "Calhoun County", f"Expected 'Calhoun County', got '{public_school_fetcher.extract_county(anniston_soup)}'"
    assert public_school_fetcher.extract_county(shiloh_soup) == "Gwinnett County", f"Expected 'Gwinnett County', got '{public_school_fetcher.extract_county(shiloh_soup)}'"
    assert public_school_fetcher.extract_county(south_haven_soup) == "Van Buren County", f"Expected 'Van Buren County', got '{public_school_fetcher.extract_county(south_haven_soup)}'"

def test_extract_locale(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_locale(anniston_soup) == "City: Small (13)", f"Expected 'City: Small (13)', got '{public_school_fetcher.extract_locale(anniston_soup)}'"
    assert public_school_fetcher.extract_locale(shiloh_soup) == "Suburb: Large (21)", f"Expected 'Suburb: Large (21)', got '{public_school_fetcher.extract_locale(shiloh_soup)}'"
    assert public_school_fetcher.extract_locale(south_haven_soup) == "Town: Distant (32)", f"Expected 'Town: Distant (32)', got '{public_school_fetcher.extract_locale(south_haven_soup)}'"

def test_extract_total_students(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_total_students(anniston_soup) == 466, f"Expected 466, got {public_school_fetcher.extract_total_students(anniston_soup)}"
    assert public_school_fetcher.extract_total_students(shiloh_soup) == 2203, f"Expected 2203, got {public_school_fetcher.extract_total_students(shiloh_soup)}"
    assert public_school_fetcher.extract_total_students(south_haven_soup) == 569, f"Expected 569, got {public_school_fetcher.extract_total_students(south_haven_soup)}"

def test_extract_classroom_teachers(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_classroom_teachers(anniston_soup) == 27.5, f"Expected 27.5, got {public_school_fetcher.extract_classroom_teachers(anniston_soup)}"
    assert public_school_fetcher.extract_classroom_teachers(shiloh_soup) == 134.2, f"Expected 134.2, got {public_school_fetcher.extract_classroom_teachers(shiloh_soup)}"
    assert public_school_fetcher.extract_classroom_teachers(south_haven_soup) == 30.97, f"Expected 30.97, got {public_school_fetcher.extract_classroom_teachers(south_haven_soup)}"

def test_extract_student_teacher_ratio(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_student_teacher_ratio(anniston_soup) == 16.95, f"Expected 16.95, got {public_school_fetcher.extract_student_teacher_ratio(anniston_soup)}"
    assert public_school_fetcher.extract_student_teacher_ratio(shiloh_soup) == 16.42, f"Expected 16.42, got {public_school_fetcher.extract_student_teacher_ratio(shiloh_soup)}"
    assert public_school_fetcher.extract_student_teacher_ratio(south_haven_soup) == 18.37, f"Expected 18.37, got {public_school_fetcher.extract_student_teacher_ratio(south_haven_soup)}"

def test_extract_grade_span_public(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    assert public_school_fetcher.extract_grade_span(anniston_soup) == "9-12", f"Expected '9-12', got '{public_school_fetcher.extract_grade_span(anniston_soup)}'"
    assert public_school_fetcher.extract_grade_span(shiloh_soup) == "9-12", f"Expected '9-12', got '{public_school_fetcher.extract_grade_span(shiloh_soup)}'"
    assert public_school_fetcher.extract_grade_span(south_haven_soup) == "9-12", f"Expected '9-12', got '{public_school_fetcher.extract_grade_span(south_haven_soup)}'"

def test_extract_enrollment_by_race(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    anniston_expected = {
        'American Native': 0,
        'Asian': 1,
        'Black': 392,
        'Hispanic': 34,
        'Pacific Islander': 0,
        'White': 22,
        'Multiple Races': 17
    }
    shiloh_expected = {
        'American Native': 2,
        'Asian': 78,
        'Black': 1476,
        'Hispanic': 512,
        'Pacific Islander': 1,
        'White': 73,
        'Multiple Races': 61
    }
    south_haven_expected = {
        'American Native': 3,
        'Asian': 5,
        'Black': 55,
        'Hispanic': 112,
        'Pacific Islander': 0,
        'White': 332,
        'Multiple Races': 62
    }
    assert public_school_fetcher.extract_enrollment_by_race(anniston_soup) == anniston_expected, f"Expected {anniston_expected}, got {public_school_fetcher.extract_enrollment_by_race(anniston_soup)}"
    assert public_school_fetcher.extract_enrollment_by_race(shiloh_soup) == shiloh_expected, f"Expected {shiloh_expected}, got {public_school_fetcher.extract_enrollment_by_race(shiloh_soup)}"
    assert public_school_fetcher.extract_enrollment_by_race(south_haven_soup) == south_haven_expected, f"Expected {south_haven_expected}, got {public_school_fetcher.extract_enrollment_by_race(south_haven_soup)}"

def test_extract_enrollment_by_gender(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    anniston_expected = {
        'Male Enrollment': 243,
        'Female Enrollment': 223
    }
    shiloh_expected = {
        'Male Enrollment': 1200,
        'Female Enrollment': 1003
    }
    south_haven_expected = {
        'Male Enrollment': 279,
        'Female Enrollment': 290
    }
    assert public_school_fetcher.extract_enrollment_by_gender(anniston_soup) == anniston_expected, f"Expected {anniston_expected}, got {public_school_fetcher.extract_enrollment_by_gender(anniston_soup)}"
    assert public_school_fetcher.extract_enrollment_by_gender(shiloh_soup) == shiloh_expected, f"Expected {shiloh_expected}, got {public_school_fetcher.extract_enrollment_by_gender(shiloh_soup)}"
    assert public_school_fetcher.extract_enrollment_by_gender(south_haven_soup) == south_haven_expected, f"Expected {south_haven_expected}, got {public_school_fetcher.extract_enrollment_by_gender(south_haven_soup)}"

def test_extract_lunch_eligibility(public_school_fetcher, anniston_soup, shiloh_soup, south_haven_soup):
    anniston_expected = {
        'Free lunch eligible': 378,
        'Reduced lunch eligible': 23,
        'Free/reduced total eligible': 401
    }
    shiloh_expected = {
        'Free lunch eligible': 1156,
        'Reduced lunch eligible': 270,
        'Free/reduced total eligible': 1426
    }
    south_haven_expected = {
        'Free lunch eligible': 322,
        'Reduced lunch eligible': 26,
        'Free/reduced total eligible': 348
    }
    assert public_school_fetcher.extract_lunch_eligibility(anniston_soup) == anniston_expected, f"Expected {anniston_expected}, got {public_school_fetcher.extract_lunch_eligibility(anniston_soup)}"
    assert public_school_fetcher.extract_lunch_eligibility(shiloh_soup) == shiloh_expected, f"Expected {shiloh_expected}, got {public_school_fetcher.extract_lunch_eligibility(shiloh_soup)}"
    assert public_school_fetcher.extract_lunch_eligibility(south_haven_soup) == south_haven_expected, f"Expected {south_haven_expected}, got {public_school_fetcher.extract_lunch_eligibility(south_haven_soup)}"
