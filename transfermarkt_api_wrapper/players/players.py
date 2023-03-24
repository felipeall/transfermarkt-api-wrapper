from dataclasses import dataclass

from transfermarkt_api_wrapper.main import TransfermarktAPI


@dataclass
class TransfermarktPlayers(TransfermarktAPI):
    def get_market_value(self, player_id: str) -> dict:
        endpoint: str = f"players/{player_id}/market_value"

        response = self.request(endpoint=endpoint)

        return response.json()
