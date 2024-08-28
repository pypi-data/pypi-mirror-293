# Itaú UY API

A Python library for interacting with the Itaú Uruguay bank API.

## Installation

To install the package with all its dependencies to your local environment:

```
pip install .
```

For development, sync your venv with uv:

```
uv sync --all-extras --dev
```

## Usage

```python
from itau_uy_api import ItauAPI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API
api = ItauAPI(os.environ['ITAU_USER_ID'], os.environ['ITAU_PASSWORD'])

# Login
api.login()

# Get account information
for account in api.accounts:
    print(f"Account Type: {account['type']}")
    print(f"Balance: {account['balance']} {account['currency']}")

# Get transactions for the current month
from datetime import datetime
current_month = datetime.now().month
current_year = datetime.now().year
transactions = api.get_month(api.accounts[0]['hash'], current_month, current_year)

# Get credit card transactions
credit_transactions = api.get_credit_card_transactions()
```

## Development

To set up the development environment:

0. Ensure you have [uv](https://github.com/astral-sh/uv) installed and are running `Python >= 3.12`
1. Clone the repository and `cd` into it
2. Sync the virtual environment, installing dependencies with `uv sync`
3. Create a `.env` file in the root directory with the following content:
   ```
   ITAU_USER_ID=your_user_id
   ITAU_PASSWORD=your_password_base64_encoded
   ```
   Replace `your_user_id` and `your_password` with your actual Itau credentials, password should be encoded in base64.

4. Run tests:
   ```
   uv run pytest
   ```

5. Run linters and formatters:
   ```
   uv run black .
   uv run pflake8
   uv run mypy .
   ```

Note: Make sure to never commit your `.env` file to version control as it contains sensitive information.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
