# Project Implementation Status Report

Alessio Perco

20398826

Group 3

## Requirements Report


| Requirement | Function                    | Implementation Status | Missing Elements                  |
| :------------ | :---------------------------- | :---------------------- | :---------------------------------- |
| R1          | add_book_to_catalog         | Complete              | None                              |
| R2          | N/A                         | N/A                   | No function available for testing |
| R3          | borrow_book_by_patron       | Complete              | None                              |
| R4          | return_book_by_patron       | Incomplete            | Function Not Implemented          |
| R5          | calculate_late_fee_for_book | Incomplete            | Function Not Implemented          |
| R6          | search_books_in_catalog     | Incomplete            | Function Not Implemented          |
| R7          | get_patron_status_report    | Incomplete            | Function Not Implemented          |

There currently does not exist a method to create a Patron ID. This affects the validity of the tests written but does not impact the reporting in the Requirements Table above.

## Tests Scripts Summary

All tests were written to account for as many different scenarios as possible given the limited implementation of many of the requirements. Each requirement has at least 4-5 test cases including positive and negative test cases.

### R1: R1tests.py

These tests interact with add_book_to_catalog by experimenting with valid inputs, incorrectly adding books by exceeding the maximum character limits for the title and author name, and incorectly adding a book with an invalid ISBN. Additionally, one test attempts incorrectly to add a book with a negative number of copies

### R2: R2tests.py

These tests interact with what I would be the implementation of a catalog reader function, designed so that tests and other functions could read the state of elements of the catalog. It includes looking for Book ID's, Titles, Authors and IBSNs. Additionally, it checks the number of total copies and available copiesin separate tests, and checks whether or not the Borrow button works properly depending on whether or not a book has available copies.

### R3: R3tests.py

These tests interact with borrow_book_by_patron by testing for a book checkout given valid inputs, trying to check out a book when it is not available, and more. The add_book_to_catalog function is briefly used to make more available books when testing that a single patron cannot check out more than 5 books. However, this function is not the focus of this group of tests. This file also tests for trying to borrow a book with an invalid patron ID.

### R4: R4tests.py

These tests are designed to interact with a completed return_book_by_patron function. It tests for a normal valid book return, and invalid returns through an invalid patron ID, invalid ISBN, or the case where the listed book was not borrowed by the patron.

### R5: R5tests.py

These tests are designed to interact with a completed calculate_late_fee_for_book_function. It tests with a base valid input for a theoretically late book, valid input for a book that is not late, and additional invalid inputs. These include testing for inputting an invalid ISBN or inputting an invalid patron ID.

### R6: R6tests.py

These tests are designed to interact with a completed search_books_in_catalog function. This includes trying valid searches for a title, author, and ISBN separately. It also tries to search for an invalid ISBN.

### R7: R7tests.py

These tests are designed to interact with a completed get_patron_status_report function. This includes attempting to get a valid overall status report, a valid borrowing history, and test getting a status report by using a patron ID that is too short or simply does not exist.
