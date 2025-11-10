import pytest
from services.library_service import (
    calculate_late_fee_for_book, get_book_by_id, pay_late_fees, refund_late_fee_payment
)
from unittest.mock import Mock
from services.payment_service import PaymentGateway

#PAY_LATE_FEES()
#pay_late_fees(patron_id: str, book_id: int, payment_gateway: PaymentGateway = None) -> Tuple[bool, str, Optional[str]]

#successful payment
def test_pay_late_fees_successful_payment(mocker):
    '''Test paying a late fee successfully'''

    mocker.patch('services.library_service.get_book_by_id', return_value={'title':'Test Book', 'author':'Test Author', 'isbn':1234567890124, 'total_copies':5})
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':2.00, 'days_overdue': 4, 'status': 'Late fee calculation completed successfully.'})

    # In tests, mock the payment gateway:
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, 'txn_123', 'Success')
    success, msg, txn = pay_late_fees("123456", 5, mock_gateway)

    #mock_gateway.process_payment.assert_called_with(patron_id="123456", amount=2.00, description="Late fees for 'Test Book'")
    mock_gateway.process_payment.assert_called_once()
    assert success is True
    assert 'success' in msg.lower()
    assert txn == 'txn_123'


#payment declined by gateway
def test_pay_late_fee_unsuccessful_declined_by_gateway(mocker):
    '''Test how the function reacts when the gateway denies its request'''

    mocker.patch('services.library_service.get_book_by_id', return_value={'title':'Test Book', 'author':'Test Author', 'isbn':1234567890124, 'total_copies':5})
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':1000, 'days_overdue': 4, 'status': 'Late fee calculation completed successfully.'})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")
    success, msg, txn = pay_late_fees("123456", 5, mock_gateway)

    mock_gateway.process_payment.assert_called_once()
    assert success is False
    assert 'failed: payment declined' in msg.lower()
    assert txn is None

#invalid patron ID (verify mock NOT called)
def test_pay_late_fee_unsuccessful_invalid_patron_id(mocker):
    '''Test that the function fails when handed an invalid patron ID'''

    mocker.patch('services.library_service.get_book_by_id', return_value={'title':'Test Book', 'author':'Test Author', 'isbn':1234567890124, 'total_copies':5})
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':2.00, 'days_overdue': 4, 'status': 'Late fee calculation completed successfully.'})

    # In tests, mock the payment gateway:
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, 'txn_123', 'Success')
    success, msg, txn = pay_late_fees("123456789", 5, mock_gateway)
    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert 'invalid patron id. must be exactly 6 digits.' in msg.lower()
    assert txn is None

#zero late fees (verify mock NOT called)
def test_pay_late_fees_zero_late_fees(mocker):
    '''Test that the mock is not called when there are zero late fees'''

    mocker.patch('services.library_service.get_book_by_id', return_value={'title':'Test Book', 'author':'Test Author', 'isbn':1234567890124, 'total_copies':5})
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':0.00, 'days_overdue': 0, 'status': 'Late fee calculation completed successfully.'})

    # In tests, mock the payment gateway:
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, 'txn_123', 'Success')
    success, msg, txn = pay_late_fees("123456", 5, mock_gateway)

    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert 'no late fees to pay for this book.' in msg.lower()
    assert txn is None

#network error exception handling
def test_pay_late_fees_network_error(mocker):
    '''Verify that the function can handle network erors'''

    mocker.patch('services.library_service.get_book_by_id', return_value={'title':'Test Book', 'author':'Test Author', 'isbn':1234567890124, 'total_copies':5})
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'fee_amount':2.00, 'days_overdue': 4, 'status': 'Late fee calculation completed successfully.'})

    # In tests, mock the payment gateway:
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = ConnectionError
    success, msg, txn = pay_late_fees("123456", 5, mock_gateway)

    mock_gateway.process_payment.assert_called_once()
    assert success is False
    assert 'payment processing error' in msg.lower()
    assert txn is None



#REFUND_LATE_FEE_PAYMENT()

#successful refund
def test_refund_late_fee_payment_successful_refund(mocker):
    '''Test refunding a late fee payment successfully'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $4.00 processed successfully. Refund ID: refund_txn_123")
    success, msg = refund_late_fee_payment('txn_123', 4.00, mock_gateway)

    mock_gateway.refund_payment.assert_called_once()
    assert success is True
    assert 'Refund of $4.00 processed successfully. Refund ID: refund_txn_123' in msg

#invalid transction ID rejection
def test_refund_late_fee_payment_invalid_transaction_id(mocker):
    '''Use an invalid transaction ID when calling the function. Should catch error before calling refund_payment'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid transaction ID")
    success, msg = refund_late_fee_payment('alessio was here', 4.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert 'Invalid transaction ID' in msg


#invalid refund amounts:
#negative refund amount
def test_refund_late_fee_payment_invalid_negative_refund_amount(mocker):
    '''Try and get a refund by passing a negative amount as an argument'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, msg = refund_late_fee_payment('txn_123', -4.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert 'Refund amount must be greater than 0.' in msg


#zero refund amount
def test_refund_late_fee_payment_invalid_zero_refund_amount(mocker):
    '''Try and get a refund by passing a 0 dollars as an argument'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Invalid refund amount")
    success, msg = refund_late_fee_payment('txn_123', 0, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert 'Refund amount must be greater than 0.' in msg

#refund amount exceeds $15 maximum
def test_refund_late_fee_payment_invalid_exceeds_maximum(mocker):
    '''Try and get a refund while exceeding the $15 maximum'''

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $20.00 processed successfully. Refund ID: refund_txn_123")
    success, msg = refund_late_fee_payment('txn_123', 20.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert 'Refund amount exceeds maximum late fee.' in msg