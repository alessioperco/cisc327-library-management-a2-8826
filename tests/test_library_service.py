
import pytest
from services.library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report
)

# R1: Add Book To Catalog
def test_add_book_valid():
    result = add_book_to_catalog("Clean Code", "Robert C. Martin", "1234567890123", 5)
    assert result[0] is True
    assert "successfully added" in result[1]

def test_add_book_missing_title():
    result = add_book_to_catalog("", "Author", "1234567890123", 5)
    assert result == (False, "Title is required.")

def test_add_book_long_title():
    result = add_book_to_catalog("A" * 201, "Author", "1234567890123", 5)
    assert result == (False, "Title must be less than 200 characters.")

def test_add_book_invalid_isbn():
    result = add_book_to_catalog("Title", "Author", "123", 5)
    assert result == (False, "ISBN must be exactly 13 digits.")

def test_add_book_negative_copies():
    result = add_book_to_catalog("Title", "Author", "1234567890123", -1)
    assert result == (False, "Total copies must be a positive integer.")

# R3: Book Borrowing Interface
def test_borrow_book_valid():
    result = borrow_book_by_patron("123456", 1)
    assert result[0] is True
    assert "Successfully borrowed" in result[1]

def test_borrow_book_invalid_patron_id():
    result = borrow_book_by_patron("abc123", 1)
    assert result == (False, "Invalid patron ID. Must be exactly 6 digits.")

def test_borrow_book_unavailable():
    result = borrow_book_by_patron("123456", 999)
    assert result == (False, "Book not found.")

# R4: Book Return Processing
def test_return_book_valid():
    result = return_book_by_patron("123456", 1)
    assert result[0] is True
    assert "Successfully returned" in result[1]

def test_return_book_invalid_patron_id():
    result = return_book_by_patron("12", 1)
    assert result == (False, "Invalid patron ID. Must be exactly 6 digits.")

def test_return_book_not_borrowed():
    result = return_book_by_patron("123456", 999)
    assert result == (False, "Book not borrowed by patron.")

# R5: Late Fee Calculation API
def test_late_fee_no_overdue():
    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 0.00
    assert result["days_overdue"] == 0

def test_late_fee_invalid_patron_id():
    result = calculate_late_fee_for_book("abc", 1)
    assert result["status"].startswith("Late fee calculation failed")

# R6: Book Search Functionality
def test_search_by_title_partial_match():
    results = search_books_in_catalog("clean", "title")
    assert any("Clean Code" in book["title"] for book in results)

def test_search_by_isbn_exact_match():
    results = search_books_in_catalog("1234567890123", "isbn")
    assert len(results) == 1
    assert results[0]["isbn"] == "1234567890123"

# R7: Patron Status Report
def test_patron_status_valid():
    result = get_patron_status_report("123456")
    assert result["status"].startswith("Successfully")
    assert isinstance(result["borrowed_books"], list)

def test_patron_status_invalid_id():
    result = get_patron_status_report("abc")
    assert result["status"].startswith("Failed")
