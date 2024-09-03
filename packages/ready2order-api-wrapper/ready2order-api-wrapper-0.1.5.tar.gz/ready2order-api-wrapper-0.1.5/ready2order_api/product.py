import requests
import pandas as pd

class Product:
    def __init__(self, account_token):
        self.account_token = account_token
        self.base_url = "https://api.ready2order.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.account_token}",
            "Content-Type": "application/json"
        }

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