import asyncio
import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, ClassVar, Coroutine, TypedDict, overload
import httpx
from .baseball_savant import Client, HittingStats, PitchingStats, StatCast


__all__: list[str] = ["Player", "PlayerDict"]


class PlayerDict(TypedDict):
    id: int
    firstname: str
    lastname: str
    slug: str
    url: str
    statcast: StatCast


@dataclass
class Player:

    SEP: ClassVar[str] = ", "
    BASE_URL: ClassVar[str] = "https://baseballsavant.mlb.com/savant-player/"

    def __init__(
        self,
        id: str,
        fullname: str,
        semaphore: asyncio.Semaphore = asyncio.Semaphore(100),
    ) -> None:
        if self.SEP not in fullname:
            raise ValueError("Not a player")
        self.id: int = int(id)
        self.fullname: str = fullname
        self.semaphore: asyncio.Semaphore = semaphore
        self.client: Client = Client(self)

    @property
    def firstname(self) -> str:
        return self.fullname.split(self.SEP)[-1]

    @property
    def lastname(self) -> str:
        return self.fullname.split(self.SEP)[0]

    @property
    def slug(self) -> str:
        return "-".join([self.firstname, self.lastname, str(self.id)]).lower()

    @property
    def url(self) -> str:
        return f"{self.BASE_URL}{self.slug}"

    @cached_property
    def statcast(self) -> StatCast:
        return {"hitting": self.hitting, "pitching": self.pitching}

    @cached_property
    def pitching(self) -> dict[str, PitchingStats]:
        return self.client.get_pitching()

    @cached_property
    def hitting(self) -> dict[str, HittingStats]:
        return self.client.get_hitting()

    def __repr__(self) -> str:
        return (
            f'<Player(id={self.id}, lastname="{self.lastname}", '
            f'firstname="{self.firstname}")>'
        )

    def to_dict(self) -> PlayerDict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "slug": self.slug,
            "url": self.url,
            "statcast": self.statcast,
        }

    def to_json(self, file: Path | None = None) -> bytes:
        data: bytes = json.dumps(self.to_dict()).encode("utf-8")
        if file:
            file.write_bytes(data)
        return data

    @overload
    def get_stats(self) -> StatCast: ...

    @overload
    async def get_stats(self, session: httpx.AsyncClient) -> StatCast: ...

    def get_stats(
        self, session: httpx.AsyncClient | None = None
    ) -> StatCast | Coroutine[Any, Any, StatCast]:
        if session is not None:
            return self.client.get_stats(session)
        else:
            return self.client.get_stats_sync()
