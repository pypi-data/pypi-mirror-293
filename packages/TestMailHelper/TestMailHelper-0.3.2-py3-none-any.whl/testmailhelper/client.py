import requests

class TMClient:
    def __init__(self, api_key, namespace):
        """
        Initialize the TMClient with API key and namespace.

        :param api_key: Your API key for the Testmail API.
        :param namespace: The namespace for the Testmail API.
        """
        self.api_key = api_key
        self.namespace = namespace
        self.base_url = "https://api.testmail.app/api/json"

    def get_emails_list(self):
        """
        Retrieve a list of emails from the Testmail API.

        :return: A list of dictionaries, each representing an email with keys:
                 'from', 'subject', 'tag', 'timestamp', 'id'.
        :raises ValueError: If the API response is not valid JSON.
        :raises requests.exceptions.RequestException: For any issues with the HTTP request.
        """
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve emails list: {e}")
        
        try:
            response_data = response.json()
        except ValueError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        email_list = []
        all_emails = response_data.get('emails', [])
        for email in all_emails:
            email_list.append({
                'from': email.get('from', 'N/A'),
                'subject': email.get('subject', 'No Subject'),
                'tag': email.get('tag', 'No Tag'),
                'timestamp': email.get('timestamp', 'N/A'),
                'id': email.get('id', 'N/A')
            })

        return email_list

    def get_email_by_id(self, email_id):
        """
        Retrieve a specific email by its ID from the Testmail API.

        :param email_id: The ID of the email to retrieve.
        :return: A dictionary representing the email, or None if not found.
        :raises ValueError: If the API response is not valid JSON.
        :raises requests.exceptions.RequestException: For any issues with the HTTP request.
        """
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve email with ID {email_id}: {e}")

        try:
            response_data = response.json()
        except ValueError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        for email in response_data.get('emails', []):
            if email.get('id') == email_id:
                return email

        return None

    def get_emails_by_tag(self, tag):
        """
        Retrieve a list of emails with a specific tag from the Testmail API.

        :param tag: The tag to filter emails by.
        :return: A list of dictionaries, each representing an email with keys:
                 'from', 'subject', 'tag', 'timestamp', 'id'.
        :raises ValueError: If the API response is not valid JSON.
        :raises requests.exceptions.RequestException: For any issues with the HTTP request.
        """
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to retrieve emails with tag {tag}: {e}")

        try:
            response_data = response.json()
        except ValueError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        email_list = []
        all_emails = response_data.get('emails', [])
        for email in all_emails:
            if email.get('tag') == tag:
                email_list.append({
                    'from': email.get('from', 'N/A'),
                    'subject': email.get('subject', 'No Subject'),
                    'tag': email.get('tag', 'No Tag'),
                    'timestamp': email.get('timestamp', 'N/A'),
                    'id': email.get('id', 'N/A')
                })

        return email_list
