import re
from datetime import datetime
from typing import Union
from urllib.parse import quote

from .dataclass import DDPlayer, Master, Player, Query, DMap, DDStatsSql, DDStatus
from .deflt import API

REG_SERVER = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

__all__ = (
    "utc_times",
    "DDnetApi",
    "DDstats",
    "DDStatsDB"
)


def utc_times(timestamp: int | float) -> datetime:
    return datetime.utcfromtimestamp(timestamp)


class DDStatsDB(API):
    @staticmethod
    def powered() -> str:
        return 'ddstats.org'

    async def _rt(self, url: str):
        return await self._generate(url, DDStatsSql)

    async def next(self, dd: DDStatsSql):
        return await self._rt(dd.next_url)

    async def sql(self, sql: str):
        return await self._rt(f"https://db.ddstats.org/ddnet-7b306cf?sql={quote(sql)}")

    async def mapinfo(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/mapinfo.json")

    async def teamrace(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/teamrace.json")

    async def race(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/race.json")

    async def maps(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/maps.json")


class DDnetApi(API):
    @staticmethod
    def powered() -> str:
        return 'ddnet.org'

    async def player(self, player: str) -> Union[DDPlayer, None]:
        return await self._generate(f"https://ddnet.org/players/?json2={quote(player)}", DDPlayer,
                                    emoji=self._get_emoji(player))

    async def status(self) -> Union[DDStatus, None]:
        return await self._generate("https://ddnet.org/status/json/stats.json", DDStatus)

    async def query(self, player: str) -> Union[Query, None]:
        return await self._generate(f"https://ddnet.org/players/?query={quote(player)}", Query, "data",
                                    emoji=self._get_emoji(player))

    async def master(self) -> Union[Master, None]:
        return await self._generate("https://master1.ddnet.org/ddnet/15/servers.json", Master)

    async def map(self, map_name: str) -> Union[DMap, None]:
        return await self._generate(f"https://ddnet.org/maps/?json={quote(map_name)}", DMap)


class DDstats(API):
    @staticmethod
    def powered() -> str:
        return 'ddstats.tw'

    async def player(self, nickname) -> Union[Player, None]:
        return await self._generate(f"https://ddstats.tw/player/json?player={quote(nickname)}", Player, emoji=self._get_emoji(nickname))
