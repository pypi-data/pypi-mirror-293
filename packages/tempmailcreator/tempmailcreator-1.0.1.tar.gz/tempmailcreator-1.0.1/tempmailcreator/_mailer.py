import requests
import string
import random
class Lmi():
    @staticmethod
    def domains():
        return _domains()
    @staticmethod
    def get_sms(auth, page: int = 1):
        return _sms(auth=auth, page=page)
    @staticmethod
    def register(email=None, password=None):
        return _reg(address=email, password=password)
    @staticmethod
    def get_token(email, password):
        return _tkn(email, password)

def _domains() -> None:
    """ Get Domains availables """
    response = requests.get("https://api.mail.tm/domains")
    response.raise_for_status()
    return [item['domain'] for item in response.json().get('hydra:member', [])]

def _sms(auth: str, page: int = 1) -> None:
    """ Get SMS by page """
    response = requests.get("https://api.mail.tm/messages", 
                            params={"page": page}, 
                            headers={'Authorization': f'Bearer {auth}'})
    response.raise_for_status()
    messages_list = []

    for message in response.json().get("hydra:member", []):
        title = message.get("subject", "No title")
        intro = message.get("intro", "No intro")
        sender = message.get("from", {}).get("name", "No sender")
        messages_list.append({'By': sender, 'Title': title, 'Message': intro})

    return messages_list
def _reg(address: str = None, password: str = None) -> None:
    """ Register new account """
    if not address:
        domains = _domains()
        if not domains:
            raise Exception("No domains available")
        domain = random.choice(domains)
        address = f"{_genData()}@{domain}"
    if not password:
        password = _genData(12)
    response = requests.post("https://api.mail.tm/accounts", json={"address": address, "password": password})
    response.raise_for_status()
    return {'email':address, 'password':password}
def _tkn(address=str, password=str):
    response = requests.post("https://api.mail.tm/token", json={"address": address, "password": password})
    response.raise_for_status()
    return response.json()['token']
def _genData(length=10):
    """ Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))