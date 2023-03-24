from dataclasses import dataclass

import pandas as pd

from transfermarkt_api_wrapper.main import TransfermarktAPI


@dataclass
class TransfermarktClubs(TransfermarktAPI):
    def get_players(self, club_id: str, season_id: str = None) -> dict:
        endpoint: str = f"clubs/{club_id}/players"
        params: dict = {"season_id": season_id}

        response = self.request(endpoint=endpoint, params=params)

        return response.json()

    def get_players_df(self, club_id: str, season_id: str = None) -> pd.DataFrame:
        response = self.get_players(club_id=club_id, season_id=season_id)

        return pd.DataFrame(response.get("players"))
