import requests
import pandas as pd

class Ready2OrderAPI:
    def __init__(self, account_token=None):
        """
        Initialize the API client with the provided Account-Token.

        :param account_token: str, the Account-Token provided by the user.
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

    def get_products(self, as_dataframe=True):
        """
        Fetch and return products from the API.

        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :return: pd.DataFrame or dict, a DataFrame containing the products data or raw JSON.
        """
        url = f"{self.base_url}/products"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            products = response.json()
            if as_dataframe:
                return pd.DataFrame(products)
            return products
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_bills(self, as_dataframe=True):
        """
        Fetch and return all bills from the API.

        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :return: pd.DataFrame or dict, a DataFrame containing all bills data or raw JSON.
        """
        url = f"{self.base_url}/document/invoice"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if as_dataframe:
                return pd.DataFrame(data['invoices'])
            return data
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_invoice_by_id(self, invoice_id, as_dataframe=True):
        """
        Fetch and return a specific invoice by ID.

        :param invoice_id: int, the ID of the invoice to retrieve.
        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :return: pd.DataFrame or dict, a DataFrame containing the invoice data or raw JSON.
        """
        url = f"{self.base_url}/document/invoice/{invoice_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            invoice_data = response.json()

            if not as_dataframe:
                return invoice_data

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