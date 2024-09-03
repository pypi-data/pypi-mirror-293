import requests


class Ready2OrderAPI:
    def __init__(self, account_token):
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

    def create_invoice(self, data):
        """
        Create a new invoice.

        :param data: dict, the invoice data to be sent in the request.
        :return: dict, JSON response from the API.
        """
        url = f"{self.base_url}/document/invoice"
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    # Additional methods can be added here to interact with other API endpoints


