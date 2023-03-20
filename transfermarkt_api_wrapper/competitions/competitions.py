from dataclasses import dataclass
from typing import Optional

from tqdm import tqdm

from transfermarkt_api_wrapper.main import TransfermarktAPI


@dataclass
class TransfermarktCompetitions(TransfermarktAPI):
    def get_clubs(self, competition_id: str, season_id: str = None) -> dict:
        endpoint: str = f"competitions/{competition_id}/clubs"
        params: dict = {"season_id": season_id}

        response = self.request(endpoint=endpoint, params=params)

        return response.json()

    def get_players(self, competition_id: str, season_id: str = None):
        clubs = self.get_clubs(competition_id=competition_id, season_id=season_id)
        clubs_ids = [club.get("id") for club in clubs.get("clubs")]

        clubs_players = []
        for club_id in tqdm(clubs_ids):
            response = self.request(endpoint=f"clubs/{club_id}/players", params={"season_id": season_id})
            clubs_players.append(response.json())

        return clubs_players

    def get_players_market_value(self, competition_id: str, season_id: Optional[str] = None) -> list[dict]:
        players: list = self.get_players(competition_id=competition_id, season_id=season_id)
        players_ids: list = [player.get("id") for club in players for player in club.get("players")]

        players_market_value = []
        for player_id in tqdm(players_ids):
            response = self.request(endpoint=f"players/{player_id}/market_value")
            players_market_value.append(response.json())

        return players_market_value
