import logging
from typing import Any, Dict, List, Optional

import requests


class Personio:
    URL: str = "https://api.personio.de/v1"

    def __init__(
        self, client_id: str, client_secret: str, url: Optional[str] = None
    ) -> None:
        self.url = self.URL
        if url is not None:
            self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        try:
            self.token = self.get_token()
        except requests.exceptions.HTTPError as exc:
            logging.exception(exc)
            self.token = None

    def get_token(self) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Accept": "application/json"}

        response = requests.request(
            "POST", url=f"{self.url}/auth", headers=headers, data=payload
        )
        response.raise_for_status()
        return response.json()["data"]["token"]

    def get_people(self) -> List[Dict[Any, Any]]:
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}",
        }
        url = f"{self.url}/company/employees"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["data"]
