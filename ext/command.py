# import discord

from discord.ext import commands
from ext.tool import CogExt, goshujin


class Command(CogExt):

    # Goshujin only
    @commands.command()
    async def _ping(self, ctx):
        if not goshujin(ctx=ctx): return
        await ctx.send(f"{round(self.bot.latency * 1000)} (ms)")
    
    @commands.command()
    async def _del(self, ctx, lim="1"):
        if not goshujin(ctx=ctx): return
        await ctx.channel.purge(limit=int(lim) + 1)


    # everyone
    @commands.command()
    async def help(self, ctx):
        await ctx.send("help")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Command(bot))
    