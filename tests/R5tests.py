import pytest
from services.library_service import (
    calculate_late_fee_for_book, borrow_book_by_patron
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py

def test_calculate_late_fee_valid_input():
    """Test late fee calculation with valid input"""
    success = calculate_late_fee_for_book("123456", 1) #The Great Gatsby

    assert 'success' in success['status'].lower()

def test_calculate_late_fee_valid_input_book_not_late():
    """Test late fee calculation with valid input and the book is not late"""
    borrow_book_by_patron("123456", 2)
    success = calculate_late_fee_for_book("123456", 2) #To Kill A Mockingbird

    assert 'success' in success['status'].lower()
    assert success['days_overdue'] == 0
    assert success['fee_amount'] == 0.00

def test_calculate_late_fee_book_not_exist():
    """Test late fee calculation with a book that does not exist""" 
    success = calculate_late_fee_for_book("123456", 97897499)

    assert 'success' not in success['status'].lower()

def test_calculate_late_fee_invalid_patron_id_invalid():
    """Test late fee calculation with an invalid patron id""" 
    success = calculate_late_fee_for_book("123", 2) #To Kill A Mockingbird

    assert 'success' not in success['status'].lower()