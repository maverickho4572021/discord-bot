import json

# from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded
from ext.tool import goshujin
from fnmatch import fnmatch


with open(f"./__settings__.json", mode="r", encoding="utf8") as json_file:
    settings = json.load(json_file)

class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.asleep = False
        for ext in settings["extension"]:
                self.bot.load_extension(f"ext.{ext}")

    @commands.command()
    async def _l(self, ctx, ext):
        if not goshujin(ctx=ctx): return
        if ext == "load": ext = None
        try:
            self.bot.load_extension(f"ext.{ext}")
            await ctx.message.add_reaction("🆗")
        except ExtensionNotFound:
            await ctx.message.add_reaction("⚠️")

    @commands.command()
    async def _ul(self, ctx, ext):
        if not goshujin(ctx=ctx): return
        if ext == "load": ext = None
        try:
            self.bot.unload_extension(f"ext.{ext}")
            await ctx.message.add_reaction("🆗")
        except ExtensionNotLoaded:
            await ctx.message.add_reaction("⚠️")

    @commands.command()
    async def _rl(self, ctx, ext):
        if not goshujin(ctx=ctx): return
        if ext == "load": ext = None
        try:
            self.bot.reload_extension(f"ext.{ext}")
            if ext == "EMJ":
                await ctx.message.add_reaction("<a:loading:866600939234132018>")
            else:
                await ctx.message.add_reaction("🆗")
        except ExtensionNotLoaded:
            await ctx.message.add_reaction("⚠️")

def setup(bot):
    bot.add_cog(Load(bot))