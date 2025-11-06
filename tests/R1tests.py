import pytest
from services.library_service import (
    add_book_to_catalog
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py


def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()


def test_add_book_invalid_title_too_long():
    """Test adding a book with title too long."""
    success, message = add_book_to_catalog("TooLongHaha"*200, "Test Author", "1234567890123", 5)

    assert success == False
    assert "title must be less than 200 characters." in message.lower()

def test_add_book_invalid_author_too_long():
    """Test adding a book with author name too long."""
    success, message = add_book_to_catalog("Test Book", "Woah this name is too long"*100, "1234567890123", 5)

    assert success == False
    assert "author must be less than 100 characters" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message.lower()


def test_add_book_total_copies_negative_integer():
    """Test adding a book with a negative number of copies"""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", -4)

    assert success == False
    assert "total copies must be a positive integer." in message.lower()

