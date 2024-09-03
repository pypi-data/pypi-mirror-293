from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class UserStats:
    _id: str
    """Returns the ID of the user."""
    coins: int
    """Returns the coins of the user."""
    claimed: datetime
    """Returns the last datetime, when the user claimed his daily coins. Returns 'Never', when the user never claimed his daily coins before."""
    streak: int
    """Returns the user's current daily streak."""
    max_streak: int
    """Returns the user's max daily streak."""
    pickaxe_level: int
    """Returns the user's pickaxe level."""
    smelter_level: int
    """Returns the user's smelters level."""
    luck: int
    """Returns the user's luck level."""
    shields: int
    """Returns the user's amount of shields."""
    cooldown_pickaxe: datetime
    """Returns the last datetime, when the user mined stone."""
    cooldown_smelter: datetime
    """Returns the last datetime, when the user fired up his smelter."""
    maxInventorySize: int
    """Returns the maximum inventory size of the user."""
    inventory: List[str] = field(default_factory=list)
    """Returns the inventory of the user."""

    @property
    def id(self) -> str:
        """Returns the ID of the user."""
        return self._id


@dataclass
class GuildStats:
    _id: str
    language: str
    """Returns the language of the guild."""
    in_guild: bool
    """Returns if the bot is on the guild."""
    enabled_modules: List[str] = field(default_factory=list)
    """Returns the enabled modules of the guild."""
