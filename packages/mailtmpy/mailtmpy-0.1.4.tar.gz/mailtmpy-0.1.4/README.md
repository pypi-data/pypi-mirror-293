# MailTM API Wrapper

<!-- [![Downloads](https://pepy.tech/badge/mailtm)](https://pepy.tech/project/mailtm)

[![Downloads](https://pepy.tech/badge/mailtm/month)](https://pepy.tech/project/mailtm)
[![Downloads](https://pepy.tech/badge/mailtm/week)](https://pepy.tech/project/mailtm) -->

MailTm is a free temporary mail service, This fork of library, thats is useful for automation tasks such as making accounts that needs email verification.
New in fork:
- Pydantic models for messages and credentials on register
- Waiting for mew message
- Return credentials for new registered account
- Login method

## Installation

Windows:

```
pip install mailtmpy
```

Linux/Mac OS:

```
pip3 install mailtmpy
```

## Example

```python
from mailtmpy import Email

def listener(message):
    print("\nSubject: " + message['subject'])
    print("Content: " + message['text'] if message['text'] else message['html'])

# Get Domains
test = Email()
print("\nDomain: " + test.domain)

# Make new email address
test.register()
print("\nEmail Adress: " + str(test.address))

# Start listening
test.start(listener)
print("\nWaiting for new emails...")

# Wait for new message
new_message = test.wait_for_new_message()
print("New message:", new_message)
```

# Documentation

API: https://mail.tm

`register(username=None, password=None, domain=None)` | Make an email account with random credentials, You can also pass a username, password and domain to use the same account.

`start(listener, interval=3)` | Start listening for new emails, Interval means how many seconds takes to sync, And you also need to pass a function for `listener`, This function gets called when new email arrive.

`stop()` | Stop listening for new emails.
