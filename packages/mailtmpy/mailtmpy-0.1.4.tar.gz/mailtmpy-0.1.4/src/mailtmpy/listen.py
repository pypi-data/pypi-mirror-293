from typing import Callable, Union
import time
from threading import Thread, Event

from requests import Session
import requests

from .models import ShortMessage, Message


class Listen:
    listen = False
    message_ids = []
    new_message_event: Event
    token: str
    listener: Union[None, Callable]
    session: Session

    def __init__(self):
        self.new_message_event = Event()
        self.session = requests.Session()

    def new_messages_list(self) -> list[ShortMessage]:
        url = "https://api.mail.tm/messages"
        headers = {'Authorization': 'Bearer ' + self.token}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return [
            ShortMessage(**msg) for i, msg in enumerate(data['hydra:member'])
            if data['hydra:member'][i]['id'] not in self.message_ids
        ]

    def message(self, id) -> Message:
        url = "https://api.mail.tm/messages/" + id
        headers = {'Authorization': 'Bearer ' + self.token}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()

        return Message(**response.json())

    def run(self) -> None:
        while self.listen:
            for message in self.new_messages_list():
                self.message_ids.append(message.id)

                if self.listener:
                    message = self.message(message.id)
                    self.listener(message)

                self.new_message_event.set()

            time.sleep(self.interval)

    def start(self, listener=None, interval=3) -> None:
        if self.listen:
            self.stop()

        self.listener = listener
        self.interval = interval
        self.listen = True

        # Start listening thread
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self) -> None:
        self.listen = False
        self.thread.join()

    def wait_for_new_message(self) -> Message:
        self.new_message_event.wait()
        self.new_message_event.clear()

        return self.message(self.message_ids[-1])
