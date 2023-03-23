import logging
from dataclasses import dataclass, field

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logging.basicConfig(level=logging.DEBUG)


@dataclass
class TransfermarktAPI:
    api_root: str = "https://transfermarkt-api.vercel.app"
    retry_total: int = 5
    retry_backoff: int = 2
    retry_codes: list[int] = field(default_factory=lambda: [500, 501, 502, 503, 504])

    def __post_init__(self):
        retries = Retry(
            total=self.retry_total,
            backoff_factor=self.retry_backoff,
            status_forcelist=self.retry_codes,
        )
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def request(self, endpoint: str, params: dict = None):
        url: str = f"{self.api_root}/{endpoint}"
        response: Response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response
