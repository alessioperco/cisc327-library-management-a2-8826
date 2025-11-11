import pytest
from services.library_service import (
    get_patron_status_report, borrow_book_by_patron
)
#For pytesting to work, make sure that this file is in the same directory as library_service.py

def test_get_report_valid_input():
    """""Test get a report using a valid input"""
    success = get_patron_status_report("123456")

    assert 'success' in success['status'].lower()

def test_get_report_invalid_id_too_short():
    """""Test get a report using an id that is too short"""""
    success = get_patron_status_report("123")

    assert 'invalid patron id' in success['status'].lower()

def test_get_report_valid_id_does_not_exist():
    """Test get a report using an id that does not exist"""""
    success = get_patron_status_report("999999") #assuming this id does not exist

    assert success['borrow_count'] == 0

def test_get_report_valid_book_check():
    """Test that the borrowed_books field can correctly report books"""""
    borrow_book_by_patron("123456", 4)
    report = get_patron_status_report("123456")

    success = False
    for item in report['borrowed_books']:
        if item['book_id'] == 4:
            success = True
            break

    assert success == True