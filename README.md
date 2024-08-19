# NCESchools

NCESchools is a Python package designed to search and extract detailed information about public and private schools from the NCES (National Center for Education Statistics) website. This package allows users to search for schools by name, city, state, and zip code, and extract various details such as enrollment, teacher-student ratios, and more.

## Overview

The `NCESchools` package provides the following functionalities:
- Search for public or private schools by name, location, and other parameters.
- Extract detailed school information from the NCES website.
- Handle both public and private school searches with specialized fetchers.

## Installation

### Prerequisites

- Conda (recommended for managing environments)

### Local Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GSU-Analytics/NCEShools.git
   cd NCEShools
   ```

2. **Create a Conda environment**:
   
   You can set up the environment using the `local_install.yml` file provided in the repository. This will install the required dependencies such as `requests`, `beautifulsoup4`, and `pytest`.

   ```bash
   conda env create -f local_install.yml
   ```

3. **Activate the environment**:
   ```bash
   conda activate nceshools
   ```

4. **Install the package**:
   
   After setting up the environment, you can install the `NCEShools` package in editable mode:

   ```bash
   pip install -e .
   ```

   This command installs the package in "editable" mode, meaning any changes to the source code will immediately affect the installed package.

### Remote Installation

You can also set up the `NCEShools` environment remotely using a YAML file. This method is useful if you want to import the package along with other packages from a remote repository.

1. **Create the environment**:
   Save the following YAML configuration file as `remote_install.yaml`:

   ```yaml
   name: nceshools
   channels:
     - defaults
   dependencies:
     - python>=3.11
     - pip
     - pip:
       - git+https://github.com/GSU-Analytics/NCEShools.git
   ```

2. **Install the environment**:
   ```bash
   conda env create -f remote_install.yaml
   ```

3. **Activate the environment**:
   ```bash
   conda activate nceshools
   ```

This method allows you to install the `NCEShools` package directly from the GitHub repository.

## Usage

Here’s how to use the `NCEShools` package to search and extract details for a public and a private school.

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

Ensure that you are in the root directory of the package when running tests.