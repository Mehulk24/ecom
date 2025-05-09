from django.test import TestCase

# Create your tests here.
l1 = {'id': 'pay_QRiX2ranZWe0aO', 'entity': 'payment', 'amount': 60000, 'currency': 'INR', 'status': 'captured', 'order_id': 'order_QRiWtYjQuqoVrJ', 'invoice_id': None, 'international': False, 'method': 'upi', 'amount_refunded': 0, 'refund_status': None, 'captured': True, 'description': 'Order Payment', 'card_id': None, 'bank': None, 'wallet': None, 'vpa': '7041614901@axisbank', 'email': 'mehulkshatriya9924@gmail.com', 'contact': '+917041614901', 'notes': [], 'fee': 1416, 'tax': 216, 'error_code': None, 'error_description': None, 'error_source': None, 'error_step': None, 'error_reason': None, 'acquirer_data': {'rrn': '146279263306', 'upi_transaction_id': 'FD28F7E5589DC7967DACDA915F71130F'}, 'created_at': 1746550661, 'upi': {'vpa': '7041614901@axisbank'}}

print(l1['id'])