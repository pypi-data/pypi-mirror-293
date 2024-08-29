from dataclasses import dataclass
from datetime import date


@dataclass
class UserStats:
    user_id: int
    coins: int
    allTimeMessages: int
    cooldownMiner: date
    cooldownSmelter: date
    dailyClaimed: date
    dailyStreak: int
    historyCoins: []
    historyMessages: []
    inventory: []
    luck: int
    maxInventorySize: int
    messages: int
    pickaxeLevel: int
    shields: int
    smelterLevel: int


@dataclass
class GuildStats:
    guild_id: int
    language: str
    in_guild: bool
    autoroles: []
    ticket_transcript: bool
    ticket_categorys: []
    ticket_embed_channel: str
    ticket_embed_id: str
    ticket_category_id: str
    enabled_modules: []
