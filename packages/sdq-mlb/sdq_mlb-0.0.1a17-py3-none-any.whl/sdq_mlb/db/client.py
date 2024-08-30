import sqlite3
from typing import ClassVar

from sdq_mlb import PlayerDict
from .. import Player
from ..baseball_savant import types


class Client:
    db_path: str = "mymlb.db"

    TABLES: ClassVar[dict[str, type]] = {
        "hitting": types.HittingStats,
        "pitching": types.PitchingStats,
        "ranking": types.StacastRanking,
    }

    @property
    def connection(self) -> sqlite3.Connection:
        connection: sqlite3.Connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()

    def create_tables(self) -> None:
        self._create_player_table()
        for name, type in self.TABLES.items():
            self.cursor.execute(self._write_sql_create(name, type))

    def _create_player_table(self) -> None:
        columns: list[str] = [
            column
            for column in self._get_columns(PlayerDict)
            if "statcast" not in column
        ]
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS player ({', '.join(columns)})")

    def _write_sql_create(self, name: str, type: type) -> str:
        columns: str = ", ".join(
            [
                *self._get_columns(type),
                "player",
                "FOREIGN KEY(player) REFERENCES player(id)",
            ]
        )
        return f"CREATE TABLE IF NOT EXISTS {name} ({columns})"

    def _get_columns(self, type: type) -> list[str]:
        return [f"`{column}`" for column in list(type.__annotations__.keys())]

    def insert_player(self, player: Player) -> sqlite3.Cursor:
        self._insert_player_meta(player)
        for table, type in self.TABLES.items():
            self._insert_player_stats(player, table, type)
        return self.cursor.execute(
            "SELECT * FROM player WHERE player(id) = %s", (player.id,)
        )

    def _insert_player_meta(self, player: Player) -> ...:
        columns: list[str] = self._get_columns(PlayerDict)
        sql: str = f"""
            INSERT INTO player({', '.join(columns)})
            VALUES ({', '.join([f':{column}' for column in columns])})
        """
        data: PlayerDict = player.to_dict()
        del data["statcast"]  # type: ignore
        self.cursor.execute(sql, data)

    def _insert_player_stats(self, player: Player, table: str, type: type) -> ...:
        columns: list[str] = self._get_columns(type)
        sql: str = f"""
            INSERT INTO table({', '.join(columns)})
            VALUES ({', '.join([f':{column}' for column in columns])})
        """
        self.cursor.execute(sql, getattr(player, table, {}))
