import pytest
from library_service import (
    borrow_book_by_patron, add_book_to_catalog
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py

def test_book_borrow_valid_input():
    """Test borrowing a book with a valid patron and book id (this gets The Great Gatsby)"""
    success, message = borrow_book_by_patron("123456", 1)

    assert success == True
    assert "successfully" in message.lower()

def test_book_borrow_invalid_too_many_books():
    """Test borrowing a book when 5 books are already borrowed"""
    borrow_book_by_patron("123456", 1) #The Great Gatsby
    borrow_book_by_patron("123456", 1) #The Great Gatsby
    borrow_book_by_patron("123456", 2) #To Kill a Mockingbird
    borrow_book_by_patron("123456", 2) #To Kill a Mockingbird
    add_book_to_catalog("R3 Book", "R3 Author", "3333333333333", 5) # Make a test book so we can exceed the 5 book limit (assuming this test is being ran completely independently)
    borrow_book_by_patron("123456", 6) #The R3 book after running R1 and R2tests
    success, message = borrow_book_by_patron("123456", 6) #The R3 book
    
    assert success == False
    assert "you have reached the maximum borrowing limit of 5 books." in message.lower()

def test_book_borow_invalid_book_not_available():
    """Test borrowing a book when the book is not available"""
    success, message = borrow_book_by_patron("123456", 3) #1984

    assert success == False
    assert "not available" in message.lower()

def test_book_borrow_invalid_patron_id_invalid():
    """Test borrowing a book when the patron id is an invalid length"""
    success, message = borrow_book_by_patron("123", 3) #To Kill a Mockingbird

    assert success == False
    assert "invalid patron id" in message.lower()