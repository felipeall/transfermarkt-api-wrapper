from dataclasses import dataclass

import pandas as pd

from transfermarkt_api_wrapper.players.players import TransfermarktPlayers


@dataclass
class TransfermarktPlayers(TransfermarktPlayers):
    def get_market_value_df(self, player_id: str) -> pd.DataFrame:
        response = self.get_market_value(player_id=player_id)

        return (
            pd.DataFrame(response.get("marketValueHistory"))
            .assign(date=lambda x: pd.to_datetime(x.date).dt.date)
            .assign(player_id=response.get("id"))
        )
