# NCESchools

**NCESchools** is a Python package designed to search for and extract detailed information about public and private schools from the NCES (National Center for Education Statistics) website. This package allows users to search for schools by name, city, state, and zip code, and retrieve various details such as enrollment, student-teacher ratios, and more.

## Overview

The `NCESchools` package offers the following functionalities:

- **Search Schools:** Search for public or private schools by name, location, and other parameters.
- **Extract School Information:** Extract detailed information directly from the NCES website.
- **Specialized Fetchers:** Handle both public and private school searches with dedicated fetchers.

This package builds on the NCES [Public](https://nces.ed.gov/ccd/schoolsearch/) and [Private](https://nces.ed.gov/surveys/pss/privateschoolsearch/index.asp) school search pages. For more information, visit [The National Center for Education Statistics (NCES)](https://nces.ed.gov/).

## Installation

### Prerequisites

- The installation instructions below are tailored for Conda users. If you prefer pip, you can install the package using the command: 

  ```bash
  pip install git+https://github.com/GSU-Analytics/NCESchools.git
  ```

### Remote Installation

The easiest way to install the `NCESchools` package is by using Conda to set up and update the package in your existing environment:

1. **Install the Package in an Existing Environment:**

   ```bash
   pip install git+https://github.com/GSU-Analytics/NCESchools.git
   ```

2. **Update the Package:**

   ```bash
   pip install git+https://github.com/GSU-Analytics/NCESchools.git -U
   ```

Alternatively, you can set up the `NCESchools` environment using a YAML file:

1. **Create the Environment:**

   Save the following YAML configuration as `remote_install.yaml`:

   ```yaml
   name: nceschools
   channels:
     - defaults
   dependencies:
     - python>=3.10
     - pip
     - pip:
         - git+https://github.com/GSU-Analytics/NCESchools.git
   ```

2. **Install the Environment:**

   ```bash
   conda env create -f remote_install.yaml
   ```

3. **Activate the Environment:**

   ```bash
   conda activate nceschools
   ```

### Local Setup Instructions

To customize or develop the `NCESchools` package, you can install it locally by following these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/GSU-Analytics/NCESchools.git
   cd NCESchools
   ```

2. **Create a Conda Environment:**

   Use the provided `local_install.yml` file to set up the environment, which will install the necessary dependencies, such as `requests`, `beautifulsoup4`, and `pytest`:

   ```bash
   conda env create -f local_install.yml
   ```

3. **Activate the Environment:**

   ```bash
   conda activate nceschools
   ```

4. **Install the Package in Editable Mode:**

   After setting up the environment, install the `NCESchools` package in editable mode:

   ```bash
   pip install -e .
   ```

   Installing in "editable" mode means any changes you make to the source code will immediately reflect in the installed package.

## Usage

Here’s how to use the `NCESchools` package to search and extract details for both public and private schools:

```python
from nceschools import SchoolSearcher, PublicSchoolFetcher, PrivateSchoolFetcher

def main():
    # Example usage for a public school
    print("Public School Search and Extraction:")
    public_searcher = SchoolSearcher(school_type='public')
    
    # Search for a public school and extract details
    school_name = "Shiloh High School"
    city = "Snellville"
    state = "GA"
    zip_code = "30039"

    print(f"Searching for {school_name} in {city}, {state}, {zip_code}...")
    public_nces_id = public_searcher.get_nces_id(school_name, city=city, state=state, zip_code=zip_code)
    
    if public_nces_id:
        print(f"Public School NCES ID: {public_nces_id}")
        
        public_fetcher = PublicSchoolFetcher()
        public_html = public_fetcher.get_public_school_html(public_nces_id)
        school_details = public_fetcher.extract_school_details(public_html)
        
        print("Extracted School Details:")
        for key, value in school_details.items():
            print(f"{key}: {value}")
    else:
        print(f"No public school found for {school_name} in {city}, {state}, {zip_code}.")

    # Example usage for a private school
    print("\nPrivate School Search and Extraction:")
    private_searcher = SchoolSearcher(school_type='private')
    
    # Search for a private school and extract details
    school_name = "Fuqua School"
    city = "Farmville"
    state = "VA"
    zip_code = "23901"

    print(f"Searching for {school_name} in {city}, {state}, {zip_code}...")
    private_nces_id = private_searcher.get_nces_id(school_name, city=city, state=state, zip_code=zip_code)
    
    if private_nces_id:
        print(f"Private School NCES ID: {private_nces_id}")
        
        private_fetcher = PrivateSchoolFetcher()
        private_html = private_fetcher.get_private_school_html(private_nces_id)
        school_details = private_fetcher.extract_school_details(private_html)
        
        print("Extracted School Details:")
        for key, value in school_details.items():
            print(f"{key}: {value}")
    else:
        print(f"No private school found for {school_name} in {city}, {state}, {zip_code}.")

if __name__ == "__main__":
    main()
```

## Running Tests

To run the unit tests, use the following command:

```bash
pytest
```