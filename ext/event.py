import json

from discord import Streaming
from discord.ext import commands
from ext.tool import CogExt


with open(f"./__settings__.json", mode="r", encoding="utf8") as json_file:
    settings = json.load(json_file)

name = settings["name"]
# join_channel_id = int(settings["join_channel_id"])
# leave_channel_id = int(settings["leave_channel_id"])

class Event(CogExt):

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=Streaming(
                name="人偶學園",
                url="https://www.youtube.com/watch?v=TGXFK8joMuk&list=PL2zTuGitn0Y_pOThitMc3_Abo2i1vn1Bo"
            )
        )

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = self.bot.get_channel(join_channel_id)
    #     bot_tag = "[bot]" if member.bot else ""
    #     print(f"{member} {bot_tag} join!\n")
    #     await channel.send(f"{member} {bot_tag} join!")

    # @commands.Cog.listener()
    # async def on_member_remove(self, member):
    #     channel = self.bot.get_channel(leave_channel_id)
    #     bot_tag = "[bot]" if member.bot else ""
    #     print(f"{member} {bot_tag} leave.\n")
    #     await channel.send(f"{member} {bot_tag} leave.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send(":pmEat:")

def setup(bot):
    bot.add_cog(Event(bot))