# Ready2Order API Wrapper

A Python wrapper for the Ready2Order API that simplifies the interaction with various endpoints provided by the Ready2Order platform.

## Current Features

- Fetch company information
- Fetch product information
- Fetch all bills (invoices)
- Fetch a specific invoice by its ID

## Installation

You can install the package via pip:

```bash
pip install ready2order-api-wrapper
```

## Usage Example

```python
from ready2order_api.api import Ready2OrderAPI as r2o

api = r2o("YOUR_ACCOUNT_TOKEN")

print(api.get_products())
```


## How to get your account token

To get your developer token go to [Ready2Order API](https://ready2order.com/en/api/), scroll to the bottom of the page and submit your email address to request the API token.

Now run the following code to get your account token:

```python
from ready2order_api import get_acct_token

get_acct_token.get_account_token("YOUR_DEVELOPER_TOKEN")


```
Now click on the URL starting with: https://my.ready2order.com/api/grantAccess/..., enter your login credentials and click login. You will be redirected to a blank page. Copy the account token from the URL and save it.
