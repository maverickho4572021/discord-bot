# import discord
import json

from discord import Embed
from discord.ext import commands
from fnmatch import fnmatch

EXT_PATH = "./ext"
GENSHIN_PATH = EXT_PATH + "/Genshin"

class GenshinSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(f"{GENSHIN_PATH}/__data__.json", mode="r", encoding="utf8") as json_file:
            self.data = json.load(json_file)
        with open(f"{GENSHIN_PATH}/__keys__.json", mode="r", encoding="utf8") as json_file:
            self.keys = json.load(json_file)

    @commands.Cog.listener()
    async def on_message(self, msg):
        name = ""
        if msg.content and msg.content[0] == "G":
            for key in self.keys:
                if fnmatch(key, f"*{msg.content[1:]}*"):
                    name = key
        else: name = msg.content

        if name in self.keys:
            # weapon
            if self.keys[name][0] == "武器":
                element = self.data[self.keys[name][0]][self.keys[name][1]][name]
                content = [f"◆獲取途徑：{element[0]}\n"]
                content.append(f"◆基礎攻擊力{element[1]}\n")
                content.append(f"◆{element[2]}\n")
                content.append(f"◆{element[3]}")
                description = "".join(content)
                url = self.keys[name][2]

            # artifact
            else:
                element = self.data[self.keys[name][0]][name]
                content = [f"◆品質：{element[0]}\n"]
                content.append(f"◆獲取途徑：{element[1]}\n")
                content.append(f"◆2件套裝：{element[2]}\n")
                content.append(f"◆4件套裝：{element[3]}")
                description = "".join(content)
                url = self.keys[name][1]

            await msg.channel.send(
                embed=Embed(
                    title=name, description=description, color=0xd4b4a5
                ).set_thumbnail(url=url)
            )
            
        elif msg.content[:2] == "原神":
            if msg.content[2:] in self.data["武器"]:
                await msg.channel.send(list(self.data["武器"][msg.content[2:]].keys()))
            elif msg.content[2:] == "聖遺物":
                await msg.channel.send(list(self.data["聖遺物"].keys()))


def setup(bot):
    bot.add_cog(GenshinSearch(bot))