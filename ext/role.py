import json
import discord

from discord.ext import commands


EXT_PATH = "./ext"
ROLE_PATH = EXT_PATH + "/Role"

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = None
        self.role = {}
      
    @commands.Cog.listener()
    async def on_ready(self):
        if self.data == None:
            await self.load_data()
        
    @commands.Cog.listener()
    async def load_data(self):
      
        with open(f"{ROLE_PATH}/__data__.json", mode="r", encoding="utf8") as json_file:
            self.data = json.load(json_file)
        with open(f"{ROLE_PATH}/__role__.json", mode="r", encoding="utf8") as json_file:
            self.role = json.load(json_file)

        guild = self.bot.get_guild(int(self.data["guild_id"]))
        ch = guild.get_channel(int(self.data["channel_id"]))
        # try:
        #     msg = await ch.fetch_message(int(self.data["message_id"]))
        #     await msg.delete()
        # except errors.NotFound:
        #     pass
        await ch.purge()

        embed = discord.Embed(
            title="選擇身分組&顏色",
            description=\
            "點擊反應貼圖即可獲得/取消角色對應的身分組\n",
            color=0xe9d9bf
        )
        
        msg = await ch.send(embed=embed)
        
        for emoji in self.role:
            await msg.add_reaction(emoji)
        
        print("Role extexsion is ready.")
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "<a:loading:866600939234132018>" and user == self.bot.user:
            if self.data == None:
                await self.load_data()
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction("🆗")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member == self.bot.user or payload.channel_id != int(self.data["channel_id"]): return

        if str(payload.emoji) in self.role:
            guild = self.bot.get_guild(int(self.data["guild_id"]))
            role = guild.get_role(int(self.role[str(payload.emoji)]))
            if any(int(self.role[str(payload.emoji)]) == role.id for role in payload.member.roles):
                await payload.member.remove_roles(role)
            else:
                await payload.member.add_roles(role)

def setup(bot):
    bot.add_cog(Role(bot))