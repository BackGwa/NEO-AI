import requests
import json

class MessageEngine:
    def __init__(self, contact: dict):
        self.contact = contact

    def raw_message(self, to: str, message: str) -> str:
        if to not in self.contact:
            return f"{to}는 없는 연락처이에요."

        response = requests.post(self.contact[to], data=json.dumps(message), headers={'Content-Type': 'application/json'})

        if response.status_code == 204:
            return f"{to}에게 메세지를 전달했어요."
        else:
            return "메세지를 전달하지 못했어요."