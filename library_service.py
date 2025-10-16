"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    Implements R4 as per requirements
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow

    Returns:
        tuple: (success: bool, message: str)
    """

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is borrowed by patron
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    borrowed_books = get_patron_borrowed_books(patron_id)
    for item in borrowed_books:
        if item['book_id']==book_id:
            break
    else:
        return False, "Book not borrowed by patron."
    
    # Calculate late fee
    late_fee = calculate_late_fee_for_book(patron_id, book_id)
    if "successfully" not in late_fee['status'].lower():
        return False, late_fee['status']
    
    # Update Available Copies
    return_success = update_book_availability(book_id,1)
    if not return_success:
        return False, "Database error occurred while updating book availability."
    
    # Record return date
    return_date = datetime.now()
    record_success = update_borrow_record_return_date(patron_id,book_id,return_date)
    if not record_success:
        return False, "Database error occured while updating book return date."

    
    return True, f'Successfully returned "{book["title"]}" on {return_date.strftime("%Y-%m-%d")}. ${late_fee['fee_amount']:,.2f} owed in late fees.'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    Implements R5 as per requirements 

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
         
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': 'Late fee calculation failed: Invalid patron ID. Must be exactly 6 digits.'
        }

    # Check if the book is borrowed and obtain the borrow date, due date, and overdue status for verification
    borrowed_books = get_patron_borrowed_books(patron_id)
    for item in borrowed_books:
        if item['book_id']==book_id:
            due_date = item['due_date']
            overdue_status = item['is_overdue']
            break
    else:
        return {
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': 'Late fee calculation failed: book not borrowed by patron.'
        }
    
    fee_amount = 0.00
    days_overdue = 0
    # Establish the late fee and days overdue
    if overdue_status is True:
        current_date = datetime.now()
        days_overdue = (current_date - due_date).days
        if days_overdue <= 7:
            fee_amount = days_overdue*0.50
        else:
            fee_amount = 3.50 + ((days_overdue-7)*1.00)
        if fee_amount > 15.00:
            fee_amount = 15.00

    return {
        'fee_amount': fee_amount,
        'days_overdue': days_overdue,
        'status': 'Late fee calculation completed successfully.'
    }

        


def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    Implement R6 as per requirements

    Args:
        search_term: string for the function to search through the database
        search_type: a string that specifies the type of identifier that the function must search with

    Returns:
        List of book structures
    """
    if (search_type == 'title') or (search_type == 'author'):
        returnlist = []
        all_books = get_all_books()
        for book in all_books:
            if search_term.lower() in book[search_type].lower():
                returnlist.append(book)
        return returnlist

    elif search_type == 'isbn':   
        book = get_book_by_isbn(search_term)
        if book != None:
            return [book]
    
    return []

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    Implement R7 as per requirements

    Args:
      patron_id: 6-digit library card ID

    Return:
        A dictionary of borrowed book information  
    """

    # Verify patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {'status':'Failed! Invalid patron ID.'}
    
    returndict = {'borrow_count':0,'borrowed_books':[],'total_late_fees':0.00}

    # Get the borrowed books
    borrowed_books = get_patron_borrowed_books(patron_id)

    #Assign late fees to books currently and store in a borrowed_books index. Calculate total late fees in the process (This might get a little messy)
    gatherer=[]
    late_fee_tally=0.00
    for book in borrowed_books:
        late_fee = calculate_late_fee_for_book(patron_id,book['book_id'])
        if "successfully" not in late_fee['status'].lower():
            return {'status':'Failed! Error in late fee calculation.'}
        book['late_fee']=late_fee
        late_fee_tally+=late_fee['fee_amount']
        gatherer.append(book)
    returndict['borrowed_books']=gatherer
    returndict['total_late_fees']=late_fee_tally

    # Add the borrow count
    returndict['borrow_count']=get_patron_borrow_count(patron_id)

    returndict['status'] = 'Successfully generated patron report!'

    return returndict
