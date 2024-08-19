import pytest
from nceschools.school_searcher import SchoolSearcher

@pytest.fixture
def public_school_searcher():
    return SchoolSearcher(school_type='public')

@pytest.fixture
def private_school_searcher():
    return SchoolSearcher(school_type='private')

def test_get_nces_id_public_school(public_school_searcher):
    nces_id = public_school_searcher.get_nces_id("Shiloh High School", city="Snellville", state="GA", zip_code="30039")
    assert nces_id == "130255001937", f"Expected '130255001937', got '{nces_id}'"

    nces_id = public_school_searcher.get_nces_id("Anniston High School", city="Anniston", state="AL", zip_code="36207")
    assert nces_id == "010009000011", f"Expected '010009000011', got '{nces_id}'"

def test_get_nces_id_private_school(private_school_searcher):
    nces_id = private_school_searcher.get_nces_id("Fuqua School", city="Farmville", state="VA", zip_code="23901")
    assert nces_id == "01434161", f"Expected '01434161', got '{nces_id}'"

    nces_id = private_school_searcher.get_nces_id("Grace Christian School", city="Mankato", state="MN", zip_code="56001")
    assert nces_id == "00704801", f"Expected '00704801', got '{nces_id}'"

def test_get_nces_id_not_found(public_school_searcher):
    nces_id = public_school_searcher.get_nces_id("Nonexistent School", city="Nowhere", state="NA", zip_code="00000")
    assert nces_id is None, f"Expected None, got '{nces_id}'"
