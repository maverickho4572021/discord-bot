import discord
import json
import os

from discord.ext import commands
from ext.tool import keep_alive


intents = discord.Intents.default()
intents.members = True

with open(f"./__settings__.json", mode="r", encoding="utf8") as json_file:
    settings = json.load(json_file)

bot = commands.Bot(
    command_prefix=settings["prefix"],
    intents=intents
    )
bot.remove_command("help")

bot.load_extension(f"ext.load")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ['TOKEN']
    bot.run(TOKEN)