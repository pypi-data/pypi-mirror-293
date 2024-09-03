import requests

import pandas as pd



class Ready2OrderAPI:
    def __init__(self, account_token=None):
        """
        Initialize the API client with the provided Account-Token or load it from the configuration file.

        :param account_token: str, the Account-Token provided by the user (optional if using config file).
        """


        self.account_token = account_token
        self.base_url = "https://api.ready2order.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.account_token}",
            "Content-Type": "application/json"
        }

    def get_company_info(self):
        """
        Retrieve information about the company associated with the Account-Token.

        :return: dict, JSON response from the API.
        """
        url = f"{self.base_url}/company"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_products(self):
        """
        Fetch and return products from the API.

        :return: pd.DataFrame, a DataFrame containing the products data.
        """
        url = f"{self.base_url}/products"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            products = response.json()
            df = pd.DataFrame(products)
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_bills(self):
        """
        Fetch and return all bills from the API.

        :return: pd.DataFrame, a DataFrame containing all bills data.
        """
        url = f"{self.base_url}/document/invoice"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['invoices'])
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_invoice_by_id(self, invoice_id):
        """
        Fetch and return a specific invoice by ID.

        :param invoice_id: int, the ID of the invoice to retrieve.
        :return: pd.DataFrame, a DataFrame containing the invoice data.
        """
        url = f"{self.base_url}/document/invoice/{invoice_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            invoice_data = response.json()

            invoice_header = invoice_data.copy()
            del invoice_header['items']

            rows = []
            for item in invoice_data['items']:
                row_data = invoice_header.copy()
                row_data.update(item)
                rows.append(row_data)

            df = pd.DataFrame(rows)
            df['invoice_timestamp'] = pd.to_datetime(df['invoice_timestamp'], format='%Y-%m-%d %H:%M:%S')
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None