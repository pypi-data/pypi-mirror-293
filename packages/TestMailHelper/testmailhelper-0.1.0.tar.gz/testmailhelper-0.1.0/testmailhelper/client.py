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
        :raises requests.exceptions.HTTPError: If the request to the API fails.
        """
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        response_data = response.json()
        email_list = []

        all_emails = response_data.get('emails', [])
        for email in all_emails:
            email_from = email.get('from', 'N/A')
            email_subject = email.get('subject', 'No Subject')
            tag_used = email.get('tag', 'No Tag')
            timestamp = email.get('timestamp', 'N/A')
            email_id = email.get('id', 'N/A')
            
            email_list.append({
                'from': email_from,
                'subject': email_subject,
                'tag': tag_used,
                'timestamp': timestamp,
                'id': email_id
            })

        return email_list

    def get_email_by_id(self, email_id):
        """
        Retrieve a specific email by its ID from the Testmail API.

        :param email_id: The ID of the email to retrieve.
        :return: A dictionary representing the email, or None if not found.
        :raises requests.exceptions.HTTPError: If the request to the API fails.
        """
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        response_data = response.json()
        
        for email in response_data.get('emails', []):
            if email.get('id') == email_id:
                return email

        return None
