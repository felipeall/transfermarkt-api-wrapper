from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from transfermarkt_api_wrapper.competitions.competitions import (
    TransfermarktCompetitions,
)


@dataclass
class TransfermarktCompetitions:
    api_root: str = "https://transfermarkt-api.vercel.app"
    retry_total: int = 5
    retry_backoff: int = 2
    retry_codes: list[int] = field(default_factory=lambda: [500, 501, 502, 503, 504])

    def __post_init__(self):
        self.transfermarkt = TransfermarktCompetitions(
            api_root=self.api_root,
            retry_total=self.retry_total,
            retry_backoff=self.retry_backoff,
            retry_codes=self.retry_codes,
        )

    def get_clubs(self, competition_id: str, season_id: Optional[str] = None) -> pd.DataFrame:
        response = self.transfermarkt.get_clubs(competition_id=competition_id, season_id=season_id)

        return (
            pd.DataFrame(response.get("clubs"))
            .assign(competition_id=response.get("id"))
            .assign(season_id=response.get("seasonID"))
        )

    def get_players(self, competition_id: str, season_id: Optional[str] = None) -> pd.DataFrame:
        clubs: list[dict] = self.transfermarkt.get_players(competition_id=competition_id, season_id=season_id)
        players: list = [y for x in clubs for y in x.get("players")]

        return pd.DataFrame(players)

    def get_players_market_value(self, competition_id: str, season_id: Optional[str] = None) -> pd.DataFrame:
        players: list = self.transfermarkt.get_players_market_value(competition_id=competition_id, season_id=season_id)

        players_market_values: list = []
        for player in players:
            player_id: str = player.get("id")
            player_name: str = player.get("playerName")
            player_mv: list = player.get("marketValueHistory")
            player_mv: list = [dict(item, **{"player_name": player_name}) for item in player_mv]
            player_mv: list = [dict(item, **{"player_id": player_id}) for item in player_mv]
            players_market_values.extend(player_mv)

        return (
            pd.DataFrame(players_market_values)
            .assign(date=lambda x: pd.to_datetime(x.date).dt.date)
            .assign(
                value=lambda x: x.value.replace({"€": "", "Th.": "000", "\.": "", "m": "0000", "k": "000"}, regex=True)
            )
            .assign(value=lambda x: pd.to_numeric(x.value, errors="coerce"))
            .assign(age=lambda x: pd.to_numeric(x.age, errors="coerce"))
            .assign(player_name=lambda x: x.player_name.astype("string"))
            .assign(player_id=lambda x: x.player_id.astype("string"))
        )
