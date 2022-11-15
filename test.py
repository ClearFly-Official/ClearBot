from datetime import datetime

import discord.utils

string = "2021-04-30T23:53Z"

print(type(datetime.fromisoformat(string.rstrip('Z'))))