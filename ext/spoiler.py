import discord
from discord.ext import commands

class Spoiler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spoiler_using = {}

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "spoiler":
            embed = discord.Embed(
                title="標記爆雷功能",
                description="```fix\n" +
                    "已經準備好了\n" +
                    "請上傳一張圖片\n```",
                color=0xd4b4a5
            )
            
            embed_msg = await msg.channel.send(embed=embed)

            embed = discord.Embed(
                    title="標記爆雷功能",
                    description="```fix\n" +
                        "處理中\n" +
                        "請稍後...```\n",
                    color=0xd4b4a5
                )
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/866600939234132018.gif")
                        
            self.spoiler_using[msg.author] = [embed_msg.channel.id, embed_msg.id, embed]
    
            await msg.delete()


        elif msg.author in self.spoiler_using and msg.attachments:
            await msg.delete()

            embed_ch = await self.bot.fetch_channel(int(self.spoiler_using[msg.author][0]))
            embed_msg = await embed_ch.fetch_message(int(self.spoiler_using[msg.author][1]))     
            await embed_msg.delete()

            embed_msg = await msg.channel.send(embed=self.spoiler_using[msg.author][2])
            file = await msg.attachments[0].to_file(spoiler=True)
            await msg.channel.send(file=file)
            await embed_msg.delete()

            del self.spoiler_using[msg.author]

def setup(bot):
    bot.add_cog(Spoiler(bot))
