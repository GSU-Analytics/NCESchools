# config.py

import sys
import os
import pytest
from bs4 import BeautifulSoup
from os.path import abspath, dirname, join
from nceschools.public_school_fetcher import PublicSchoolFetcher

# This assumes that the conftest.py file is located in the 'tests' directory
current_dir = dirname(abspath(__file__))
nceschools_dir = join(current_dir, '..', 'nceschools')
sys.path.insert(0, nceschools_dir)

def read_html_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return BeautifulSoup(content.decode('latin-1'), 'html.parser')

@pytest.fixture
def html_dir():
    # This assumes the test file is in the 'tests' directory
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'html')

# Public school fixtures
@pytest.fixture
def anniston_soup(html_dir):
    file_path = os.path.join(html_dir, 'Search for Public Schools - Anniston High School (010009000011).html')
    return read_html_file(file_path)

@pytest.fixture
def shiloh_soup(html_dir):
    file_path = os.path.join(html_dir, 'Search for Public Schools - Shiloh High School (130255001937).html')
    return read_html_file(file_path)

@pytest.fixture
def south_haven_soup(html_dir):
    file_path = os.path.join(html_dir, 'Search for Public Schools - South Haven High School (263230006770).html')
    return read_html_file(file_path)

# Private school fixtures
@pytest.fixture
def fuqua_school_soup(html_dir):
    file_path = os.path.join(html_dir, 'Search for Private Schools - School Detail for FUQUA SCHOOL.html')
    return read_html_file(file_path)

@pytest.fixture
def grace_christian_school_soup(html_dir):
    file_path = os.path.join(html_dir, 'Search for Private Schools - School Detail for GRACE CHRISTIAN SCHOOL.html')
    return read_html_file(file_path)

@pytest.fixture
def public_school_fetcher():
    return PublicSchoolFetcher()