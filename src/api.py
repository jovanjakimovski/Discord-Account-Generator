import requests
import random
import string

class GuerrillaMail:
    def __init__(self):
        self.api_url = "https://www.guerrillamail.com"
        self.email = None

    def get_email(self):
        """Fetches a temporary email address from Guerrilla Mail API."""
        response = requests.get(f"{self.api_url}/ajax.php?f=get_email_address")
        if response.status_code == 200:
            data = response.json()
            if data and 'email_addr' in data:
                self.email = data['email_addr']
                return self.email
            else:
                print("Error: No email returned from Guerrilla Mail API.")
                return None
        else:
            print(f"Error: Unable to fetch email from Guerrilla Mail API (Status Code: {response.status_code}).")
            return None

def dfilter_email(email):
    return email.replace('@', '%40').replace('.', '').replace('com', '.com')

def pfilter_email(email):
    return email.replace('@', '%40').replace('+', '%2B')

def find_email_type(email):
    if '+' in email:
        return 'plus'
    if email.count('.') > 1:
        return 'dot'
    return None
