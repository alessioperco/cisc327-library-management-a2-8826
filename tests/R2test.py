import pytest
from services.library_service import (
    placeholder_catalog_reader_function
)

def test_catalog_display_basic_information_valid():
    """Test for The Great Gatsby as the first book ID"""
    success = placeholder_catalog_reader_function()

    assert ['The Great Gatsby','F.Scott Fitzgerald','9780743273565'] in success['1']

def test_catalog_display_availability_info_valid():
    """Test for The Great Gatsby's default availability in the catalog (5 copies)"""
    success = placeholder_catalog_reader_function()

    #Check the available copies
    assert success['1'][4] == 5

def test_catalog_display_total_copies_valid():
    """Test for The Great Gatsby's default total copies in the catalog (5 copies)"""
    success = placeholder_catalog_reader_function()

    #Check the total copies
    assert success['1'][5] == 5

def test_catalog_display_button_valid():
    """Test for the borrow button for The Great Gatsby reading true as copies are available"""
    success = placeholder_catalog_reader_function()

    assert success['1'][6] == True

def test_catalog_display_button_invalid():
    """Test for the borrow button for 1984 reading true as copies are not available"""
    success = placeholder_catalog_reader_function()

    assert success['3'][6] == False