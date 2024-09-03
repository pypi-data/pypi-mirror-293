import unittest
from ready2order_api.api import Ready2OrderAPI

class TestReady2OrderAPI(unittest.TestCase):
    def setUp(self):
        self.api = Ready2OrderAPI("your_account_token")

    def test_get_company_info(self):
        response = self.api.get_company_info()
        self.assertIn("company_name", response)

    def test_create_invoice(self):
        invoice_data = {
            # Your invoice data structure here
        }
        response = self.api.create_invoice(invoice_data)
        self.assertIn("invoice_id", response)

if __name__ == "__main__":
    unittest.main()