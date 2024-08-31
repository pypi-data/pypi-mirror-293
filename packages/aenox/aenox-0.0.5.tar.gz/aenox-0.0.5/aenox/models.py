from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class UserStats:
    user_id: int
    coins: int
    claimed: datetime
    streak: int
    max_streak: int
    pickaxe_level: int
    smelter_level: int
    luck: int
    shields: int
    cooldown_pickaxe: date
    cooldown_smelter: date
    maxInventorySize: int
    inventory: []


@dataclass
class GuildStats:
    guild_id: int
    language: str
    in_guild: bool
    enabled_modules: []
