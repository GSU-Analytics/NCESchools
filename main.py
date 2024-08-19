# main.py

"""
Main script for searching and extracting school details from the NCES database.

This script demonstrates how to use the `SchoolSearcher` class and the respective
`PublicSchoolFetcher` and `PrivateSchoolFetcher` classes to search for schools
and extract detailed information based on their NCES ID.

The script performs the following tasks:
1. Searches for a public school by name, city, state, and ZIP code.
2. Retrieves the NCES ID of the public school.
3. Fetches and extracts detailed information about the public school using the NCES ID.
4. Searches for a private school by name, city, state, and ZIP code.
5. Retrieves the NCES ID of the private school.
6. Fetches and extracts detailed information about the private school using the NCES ID.

Example usage:
- The script searches for "Shiloh High School" in Snellville, GA, 30039, extracts its details, and displays them.
- It also searches for "Fuqua School" in Farmville, VA, 23901, extracts its details, and displays them.

The script is designed to be run directly as a standalone Python program.

Dependencies:
- `nceschools` package, which includes `SchoolSearcher`, `PublicSchoolFetcher`, and `PrivateSchoolFetcher`.
- `requests` and `BeautifulSoup` for handling HTTP requests and parsing HTML content.

Usage:
    $ python main.py

"""

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
