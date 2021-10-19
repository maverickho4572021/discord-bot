import json
from discord.ext import commands

EXT_PATH = "./ext"
KEYWORD_PATH = EXT_PATH + "/Keyword"

class Keyword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = None

    @commands.Cog.listener()
    async def on_ready(self):
        with open(f"{KEYWORD_PATH}/__data__.json", mode="r", encoding="utf8") as json_file:
            self.data = json.load(json_file)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not self.data:
          with open(f"{KEYWORD_PATH}/__data__.json", mode="r", encoding="utf8") as json_file:
                      self.data = json.load(json_file)
        if msg.author.bot == False and msg.content in self.data:
            await msg.channel.send(self.data[msg.content])
        
        elif msg.content[:4] == "key+":
            MCSplit = msg.content.split(" ")

            if len(MCSplit) > 3:
                await msg.add_reaction("⚠️")
                await msg.channel.send(f"格式錯誤")
                return

            if MCSplit[1] == [2]: return

            self.data[MCSplit[1]] = MCSplit[2]

            with open(f"{KEYWORD_PATH}/__data__.json", mode="w", encoding="utf8") as json_file:
                json.dump(self.data, json_file, ensure_ascii=False)
            await msg.add_reaction("🆗")

        elif msg.content[:4] == "key-":
            MCSplit = msg.content.split(" ")

            if MCSplit[1] in self.data:
                del self.data[MCSplit[1]]
                with open(f"{KEYWORD_PATH}/__data__.json", mode="w", encoding="utf8") as json_file:
                    json.dump(self.data, json_file, ensure_ascii=False)
                await msg.add_reaction("🆗")
            else:
                await msg.add_reaction("⚠️")
                await msg.channel.send(f"沒有關鍵字 {MCSplit[1]}")


def setup(bot):
    bot.add_cog(Keyword(bot))