import pytest
from services.library_service import (
    search_books_in_catalog
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py

def test_search_valid_input_title():
    """Test search for a title"""
    success = search_books_in_catalog("great","title")

    assert success[0]['title'] == 'The Great Gatsby'

def test_search_valid_input_author():
    """Test search for an author"""
    success = search_books_in_catalog("Orwell","author")

    assert success[0]['title'] == '1984'

def test_search_valid_input_isbn():
    """Test search for an isbn"""
    success = search_books_in_catalog("9780451524935","isbn")

    assert success[0]['title'] == '1984'

def test_search_invalid_isbn_invalid():
    """Test search for an invalid isbn"""
    success = search_books_in_catalog("George Orwell","isbn")

    assert success == []