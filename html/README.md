# HTML Folder Overview

This folder contains a collection of HTML files used for unit testing the NCES school information extraction tools. These files are saved from the NCES website and represent different public and private schools. They are utilized in test cases to verify the accuracy and robustness of the extraction methods implemented in the `NCESUtils`, `PublicSchoolFetcher`, and `PrivateSchoolFetcher` classes.

## Contents

- **Search for Public Schools - Anniston High School (010009000011).html**  
  - Represents Anniston High School located in Anniston, AL.
  - Used in tests for extracting public school information such as physical address, county, locale, total students, and more.

- **Search for Public Schools - Shiloh High School (130255001937).html**  
  - Represents Shiloh High School located in Snellville, GA.
  - Used in tests for verifying data extraction methods for public schools, including enrollment by race and gender, and lunch eligibility.

- **Search for Public Schools - South Haven High School (263230006770).html**  
  - Represents South Haven High School located in South Haven, MI.
  - Utilized in unit tests to validate the extraction of public school data such as student-teacher ratio and classroom teachers.

- **Search for Private Schools - School Detail for FUQUA SCHOOL.html**  
  - Represents Fuqua School, a private school located in Farmville, VA.
  - Used in unit tests for extracting private school information such as school type, physical address, grade span, and enrollment by race.

- **Search for Private Schools - School Detail for GRACE CHRISTIAN SCHOOL.html**  
  - Represents Grace Christian School, a private school located in Mankato, MN.
  - Employed in tests to ensure accurate extraction of private school details including total students, student-teacher ratio, and county.

## Usage

These HTML files serve as test data to ensure that the various extraction functions within the project can correctly parse and extract relevant information from real-world NCES HTML pages. The HTML files are intentionally diverse, covering both public and private schools, to test the full range of functionality provided by the NCES school data tools.

### Example Unit Test

Below is an example of how these HTML files are used in a unit test:

```python
def test_extract_total_students(shiloh_soup):
    assert extract_total_students(shiloh_soup) == 2203, f"Expected 2203, got {extract_total_students(shiloh_soup)}"
