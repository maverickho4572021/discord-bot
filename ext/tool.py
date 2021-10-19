import aiohttp
# import discord

from discord import AsyncWebhookAdapter
from discord import Webhook
from discord.ext import commands
from flask import Flask
from threading import Thread


GOSHUJIN_ID = 987654321

app = Flask("")

@app.route("/")
def main():
    return "Ready."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run)
    thread.start()

class CogExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def goshujin(ctx = None, msg = None):
    id = ctx.message.author.id if msg == None else msg.author.id
    return True if id == GOSHUJIN_ID else False

async def webhook_send(url, content: str = "", username: str = "", avatar_url: str = "", embed = None):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            url, 
            adapter=AsyncWebhookAdapter(session)
        )
        msg = await webhook.send(
            content=content,
            wait=True,
            username=username,
            avatar_url=avatar_url,
            embed=embed
        )
    return msg