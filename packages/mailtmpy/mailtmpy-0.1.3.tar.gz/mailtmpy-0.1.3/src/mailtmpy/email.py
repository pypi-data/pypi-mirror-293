from .helpers import username_gen, password_gen
from .listen import Listen
from .models import Credentials, Message


class EmailException(Exception):
    pass


class Email(Listen):
    domain = ""
    address = ""
    password = ""

    def __init__(self):
        super().__init__()

        if self.get_domain() is not False:
            print("Failed to get domains")

    def get_domain(self) -> str | False:
        url = "https://api.mail.tm/domains"
        response = self.session.get(url)
        response.raise_for_status()

        try:
            data = response.json()
            for domain in data["hydra:member"]:
                if domain["isActive"]:
                    self.domain = domain["domain"]
                    return self.domain

            raise Exception("No Domain")
        except Exception as e:
            raise EmailException("Failed to get domain", e)

    def register(self, username=None, password=None, domain=None) -> Credentials:
        self.domain = domain if domain else self.domain
        username = username if username else username_gen()
        password = password if password else password_gen()

        url = "https://api.mail.tm/accounts"
        payload = {"address": f"{username}@{self.domain}", "password": password}
        headers = {"Content-Type": "application/json"}
        response = self.session.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        if "address" in data:
            self.address = data["address"]
        else:
            self.address = f"{username}@{self.domain}"

        self.password = password

        self.get_token()

        if not self.address:
            raise Exception("Failed to make an address")

        return Credentials(address=self.address, password=self.password)

    def login(self, address: str, password: str) -> Credentials:
        self.address = address
        self.password = password
        self.get_token()
        return Credentials(address=self.address, password=self.password)

    def get_token(self) -> str:
        url = "https://api.mail.tm/token"
        payload = {"address": self.address, "password": self.password}
        headers = {"Content-Type": "application/json"}
        response = self.session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        try:
            self.token = response.json()["token"]
        except Exception as e:
            raise Exception("Failed to get token", e)

        return self.token


if __name__ == "__main__":

    def handler(message: Message):
        print("\nNew Message:")
        print("From:", message.from_)
        print("Subject:", message.subject)
        print("Content:", message.text if message.text else message.html)

    # Get Domains
    test = Email()
    print("\nDomain: " + test.domain)

    # Make new email address
    test.register()
    print("\nEmail Adress:", test.address)
    print("Email Password:", test.password)

    # Start listening
    test.start(handler)
    print("\nWaiting for new emails...")

    # Wait for new message
    # test.start()
    # print("\nScript execution is paused. Waiting for new email...")
    # message = test.wait_for_new_message()
    # print("New message is recieved, script execution is resumed.")
    # handler(message)

    # Stop listening
    # test.stop()
