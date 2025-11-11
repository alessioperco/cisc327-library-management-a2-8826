import pytest
from services.library_service import (
    return_book_by_patron, borrow_book_by_patron
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py

def test_book_return_valid_input():
    """Test returning a book with a valid patron and book ID"""
    success, message = return_book_by_patron("123456", 1) #The Great Gatsby

    assert success == True
    assert "successful" in message.lower()

def test_book_return_invalid_book_not_borrowed():
    """Test returning a book that the patron never borrowed"""
    success, message = return_book_by_patron("123456", 3) #1984

    assert success == False
    assert "not borrowed" in message.lower()

def test_book_return_invalid_patron_id_invalid():
    """Test returning a book when the patron id is an invalid length"""
    success, message = return_book_by_patron("123", 1) #The Great Gatsby

    assert success == False
    assert "invalid patron id" in message.lower()

def test_book_return_valid_no_late_fee():
    """Test trying to return a book without needing to pay a late fee"""
    borrow_book_by_patron("123456", 1) #The Great Gatsby
    success, message = return_book_by_patron("123456", 1)
    assert success == True
    assert "$0.00" in message.lower()
