import os
from datetime import date, datetime
from typing import overload

import httpx
from dotenv import load_dotenv

from .errors import GuildNotFound, InvalidAPIKey, NoGuildAccess, NotFound, UserNotFound, CooldownError, NoMoreCreditsAvailable
from .models import UserStats, GuildStats


def _stats_dict(data: dict[str, int]) -> dict[date, int]:
    return {datetime.strptime(d, "%Y-%m-%d").date(): count for d, count in data.items()}


class AenoXAPI:
    """A class to interact with the API of AenoX.

    Parameters
    ----------
    api_key:
        The API key to use. You can get a key by executing /api at the bot.

    Raises
    ------
    InvalidAPIKey:
        Raised when an invalid API key is provided.
    """
    def __init__(self, api_key: str):
        self.httpx_client: httpx_client = None
        self._httpx_client: httpx.Client | None = self.httpx_client

        if self.httpx_client is None:
            self._httpx_client = httpx.Client()

        self._header = {"key": api_key, "accept": "application/json"}

    def test(self) -> str:
        """Check if all worked. Returns "Success!" if it is installed correctly
        """
        return "Success!"

    @overload
    def _get(self, endpoint: str) -> dict:
        ...

    @overload
    def _get(self, endpoint: str, stream: bool) -> bytes:
        ...

    def _get(self, endpoint: str, stream: bool = False):
        response = self._httpx_client.get(
            f"https://api.aenox.xyz/v1/{endpoint}", headers=self._header
        )

        if response.status_code == 401:
            raise InvalidAPIKey()
        elif response.status_code == 403:
            raise NoGuildAccess()
        elif response.status_code == 429:
            raise CooldownError
        elif response.status_code == 404:
            response = response.json()
            message = response.get("detail")
            if "user" in message.lower() or "member" in message.lower():
                raise UserNotFound()
            elif "guild" in message.lower():
                raise GuildNotFound
            elif "credits" in message.lower():
                raise NoMoreCreditsAvailable
            raise NotFound()

        if stream:
            return response.read()

        return response.json()

    def get_user_stats(self, user_id: int) -> UserStats:
        """Get the user's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.

        Raises
        ------
        UserNotFound:
            The user was not found.
        NoMoreCreditsAvailable:
            No more credits. Check /api on Discord.
        CooldownError:
            You are on cooldown.
        """
        data = self._get(f"user/{user_id}")

        def parse_datetime(date_str: str) -> datetime:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                return None

        # Überprüfen, ob 'claimed' den Wert 0 hat
        if data.get('claimed') == 0:
            data['claimed'] = "Never"
        else:
            data['claimed'] = parse_datetime(str(data.get('claimed', '')))

        data['cooldown_pickaxe'] = parse_datetime(str(data.get('cooldown_pickaxe', '')))
        data['cooldown_smelter'] = parse_datetime(str(data.get('cooldown_smelter', '')))

        if "_id" in data:
            del data['_id']
        return UserStats(str(user_id), **data)

    def get_guild_stats(self, guild_id: int) -> GuildStats:
        """Get the user's stats.

        Parameters
        ----------
        guild_id:
            The guild's ID.

        Raises
        ------
        GuildNotFound:
            The guild was not found.
        NoMoreCreditsAvailable:
            No more credits. Check /api on Discord.
        CooldownError:
            You are on cooldown.
        """
        data = self._get(f"guild/{guild_id}")
        if "_id" in data:
            del data['_id']
        return GuildStats(str(guild_id), **data)
