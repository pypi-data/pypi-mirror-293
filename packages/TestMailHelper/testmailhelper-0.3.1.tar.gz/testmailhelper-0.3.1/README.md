# TestMailHelper

**TestMailHelper** is a Python package designed for easy interaction with the [Testmail.app API](https://testmail.app). It simplifies the process of retrieving email lists and fetching specific emails using the API.

## Features

- Retrieve a detailed list of emails from the Testmail API.
- Fetch a specific email by its ID.
- Retrieve emails filtered by a specific tag.

## Installation

This package is currently in beta. You can install it using pip:

```bash
pip install TestMailHelper==0.3.1
```

## Usage

Here's a basic example of how to use the `TMClient` class provided by the `TestMailHelper` package:

```python
from testmailhelper import TMClient

def main():
    client = TMClient(
        api_key='your_api_key',
        namespace='your_namespace'
    )
    
    # Get a list of emails
    emails = client.get_emails_list()
    print("Email List:")
    for email in emails:
        print(email)
    
    # Get a specific email by ID
    email_id = 'some_email_id'
    email = client.get_email_by_id(email_id)
    if email:
        print("Email Details:")
        print(email)
    else:
        print(f"No email found with ID: {email_id}")
    
    # Get emails by tag
    tag = 'some_tag'
    tagged_emails = client.get_emails_by_tag(tag)
    print(f"Emails with tag '{tag}':")
    for email in tagged_emails:
        print(email)

if __name__ == "__main__":
    main()
```

## API Reference

### `TMClient`

#### `__init__(api_key, namespace)`

Initialize the `TMClient` with your API key and namespace.

- `api_key` (str): Your API key for the Testmail API.
- `namespace` (str): The namespace for the Testmail API.

#### `get_emails_list()`

Retrieve a list of emails from the Testmail API.

- Returns: A list of dictionaries, each representing an email with keys: `'from'`, `'subject'`, `'tag'`, `'timestamp'`, `'id'`.
- Raises: `requests.exceptions.RequestException` if the request fails.

#### `get_email_by_id(email_id)`

Retrieve a specific email by its ID.

- `email_id` (str): The ID of the email to retrieve.
- Returns: A dictionary representing the email, or `None` if not found.
- Raises: `requests.exceptions.RequestException` if the request fails.

#### `get_emails_by_tag(tag)`

Retrieve a list of emails with a specific tag.

- `tag` (str): The tag to filter emails by.
- Returns: A list of dictionaries, each representing an email with keys: `'from'`, `'subject'`, `'tag'`, `'timestamp'`, `'id'`.
- Raises: `requests.exceptions.RequestException` if the request fails.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [Muhammad Ali](mailto:muhammad_ali@workmail.com).