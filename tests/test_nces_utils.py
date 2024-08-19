import pytest
from bs4 import BeautifulSoup
from nceschools.nces_utils import NCESUtils

def test_get_int_with_special_characters():
    assert NCESUtils.get_int("1,234 students") == 1234
    assert NCESUtils.get_int("$12,345") == 12345

def test_get_float_with_special_characters():
    assert NCESUtils.get_float_after_label(BeautifulSoup('<td>$1,234.50</td>', 'html.parser'), "Value:") is None

def test_get_int():
    assert NCESUtils.get_int("2,203") == 2203
    assert NCESUtils.get_int("abc123") == 123
    assert NCESUtils.get_int("-789") == 789
    assert NCESUtils.get_int("No numbers") is None

def test_get_text_after_label_county(anniston_soup, shiloh_soup, south_haven_soup, fuqua_school_soup, grace_christian_school_soup):
    assert NCESUtils.get_text_after_label(anniston_soup, "County:") == "Calhoun County"
    assert NCESUtils.get_text_after_label(shiloh_soup, "County:") == "Gwinnett County"
    assert NCESUtils.get_text_after_label(south_haven_soup, "County:") == "Van Buren County"
    assert NCESUtils.get_text_after_label(fuqua_school_soup, "County:") == "Prince Edward"
    assert NCESUtils.get_text_after_label(grace_christian_school_soup, "County:") == "Blue Earth"

def test_get_int_after_label_total_students(anniston_soup, shiloh_soup, south_haven_soup, fuqua_school_soup, grace_christian_school_soup):
    assert NCESUtils.get_int_after_label(anniston_soup, "Total Students:") == 466
    assert NCESUtils.get_int_after_label(shiloh_soup, "Total Students:") == 2203
    assert NCESUtils.get_int_after_label(south_haven_soup, "Total Students:") == 569
    assert NCESUtils.get_int_after_label(fuqua_school_soup, "Total Students:") == 298
    assert NCESUtils.get_int_after_label(grace_christian_school_soup, "Total Students:") == 50

def test_get_float_after_label_student_teacher_ratio(anniston_soup, shiloh_soup, south_haven_soup, fuqua_school_soup, grace_christian_school_soup):
    assert NCESUtils.get_float_after_label(anniston_soup, "Student/Teacher Ratio:") == 16.95
    assert NCESUtils.get_float_after_label(shiloh_soup, "Student/Teacher Ratio:") == 16.42
    assert NCESUtils.get_float_after_label(south_haven_soup, "Student/Teacher Ratio:") == 18.37
    assert NCESUtils.get_float_after_label(fuqua_school_soup, "Student/Teacher Ratio:") == 9.3
    assert NCESUtils.get_float_after_label(grace_christian_school_soup, "Student/Teacher Ratio:") == 7.8


