from dataclasses import dataclass
from typing import Optional

import pandas as pd

from transfermarkt_api_wrapper.players.players import TransfermarktPlayers


@dataclass
class TransfermarktPlayers(TransfermarktPlayers):
    def get_market_value_df(self, player_id: str) -> Optional[pd.DataFrame]:
        response = self.get_market_value(player_id=player_id)

        if not response.get("marketValueHistory"):
            return None

        return (
            pd.DataFrame(response.get("marketValueHistory"))
            .assign(player_id=response.get("id"))
            .assign(date=lambda x: pd.to_datetime(x.date).dt.date)
            .assign(
                value=lambda x: x["value"].replace(
                    {"€": "", "Th.": "000", "\.": "", "m": "0000", "k": "000"}, regex=True
                )
            )
        )
