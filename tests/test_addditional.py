import pytest
from services.library_service import (
    add_book_to_catalog, refund_late_fee_payment, return_book_by_patron, borrow_book_by_patron
)
from datetime import datetime
from unittest.mock import Mock
from services.payment_service import PaymentGateway

def test_add_book_invalid_no_author():
    """Test adding a book with no author"""
    success, message = add_book_to_catalog(title="Test Book", author=None, isbn="1234567890123", total_copies=5)
    
    assert success == False
    assert "Author is required." in message

def test_add_book_invalid_no_title():
    """Test adding a book with no title"""
    success, message = add_book_to_catalog(title=None, author="est Author", isbn="1234567890123", total_copies=5)
    
    assert success == False
    assert "Title is required." in message

def test_add_book_invalid_author_too_long():
    """Test adding a book with invalid author length"""
    success, message = add_book_to_catalog(title="Test Book", author="a"*200, isbn="1234567890123", total_copies=5)
    
    assert success == False
    assert "Author must be less than 100 characters." in message

''' THIS WAS PUT IN R1TEST.PY TO REPLACE THE BASIC STATIC BOOK ADDITION TEST'''
# #this is gonna just abosultely spam the library database but we're gonna change the book name based on the date and time. This will allow us to make sure we have a successful addition every time was try to add a book (the test won't fail after running once)
# def test_add_book_successful_unique():
#     """Add a unique book to the service"""

#     time=datetime.now().strftime("%Y%m%d%H%M%S")
#     uniqueisbn=time[:13]

#     success, message = add_book_to_catalog("Unique Test Book", "I'm Sorry", uniqueisbn, 5)
    
#     assert success == True
#     assert "successfully added" in message.lower()
#     #ok so im actually kind of proud of how simple this was

#network error exception handling
def test_refund_late_fee_payment_network_error(mocker):
    '''Verify that the function can handle network erors'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.side_effect = ConnectionError
    success, msg = refund_late_fee_payment('txn_123', 4.00, mock_gateway)

    mock_gateway.refund_payment.assert_called_once()
    assert success is False
    assert 'Refund processing error:' in msg

def test_book_return_book_not_borrowed():
    """Test returning a book thats not borrowed by the patron"""
    success, message = return_book_by_patron("123456", 7)

    assert success == False
    assert "Book not borrowed by patron." in message

def test_add_book_invalid_duplicate_book():
    """Test adding a duplicate book"""
    success, message = add_book_to_catalog("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 3)
    
    assert success == False
    assert "A book with this ISBN already exists." in message

def test_borrow_book_invalid_book_get(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value=False)
    success, message = borrow_book_by_patron("123456",7)
    assert success == False
    assert "book not found" in message.lower()

def test_borrow_book_too_many_books(mocker):
    mocker.patch('services.library_service.get_patron_borrow_count', return_value=7)
    success, message = borrow_book_by_patron("123456",7)
    assert success == False
    assert "reached the maximum" in message.lower()

def test_add_book_database_failure(mocker):
    time=datetime.now().strftime("%Y%m%d%H%M%S")
    mocker.patch('services.library_service.insert_book', return_value=False)
    success, message = add_book_to_catalog("Unique Test Book"+datetime.now().strftime("%S"), "I'm Sorry", "1447374155380", 5)
    assert success == False
    assert "database error" in message.lower()

def test_borrow_book_invalid_borrow_record_insert(mocker):
    mocker.patch('services.library_service.insert_borrow_record', return_value=False)
    success, message = borrow_book_by_patron("123456",7)
    assert success == False
    assert "database error" in message.lower()

def test_borrow_book_invalid_availability_check(mocker):
    mocker.patch('services.library_service.update_book_availability', return_value=False)
    success, message = borrow_book_by_patron("123456",7)
    assert success == False
    assert "database error" in message.lower()

def test_return_book_book_check_failed(mocker):
    mocker.patch('services.library_service.get_book_by_id', return_value=False)
    success, message = return_book_by_patron("123456", 7)
    assert success == False
    assert "Book not found." in message

def test_return_book_late_fee_failed(mocker):
    borrow_book_by_patron("123456", 6)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': 'boo'})
    success, message = return_book_by_patron("123456", 6)
    assert success == False
    assert "boo" in message

def test_return_book_databse_return_failed(mocker):
    borrow_book_by_patron("123456", 6)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': 'successfully'})
    mocker.patch('services.library_service.update_book_availability', return_value=False)
    success, message = return_book_by_patron("123456", 6)
    assert success == False
    assert "Database error occurred while updating book availability." in message

def test_return_book_databse_record_failed(mocker):
    borrow_book_by_patron("123456", 6)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': 'successfully'})
    mocker.patch('services.library_service.update_book_availability', return_value=True)
    mocker.patch('services.library_service.update_borrow_record_return_date', return_value=False)
    success, message = return_book_by_patron("123456", 6)
    assert success == False
    assert "Database error occured while updating book return date." in message