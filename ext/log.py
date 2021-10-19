from discord.ext import commands
from ext.tool import CogExt

LOG_GUILD_ID = 9876543210
LOG_CHANNEL_ID = 9876543210

class Log(CogExt):

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id != LOG_CHANNEL_ID:
            ctt = await self.msg_log(msg)
            await self.bot.get_guild(LOG_GUILD_ID).get_channel(LOG_CHANNEL_ID).send(ctt)
    
    async def msg_log(self, msg):
        ctt = ["```"]
        
        if msg.reference:
            ref_ch = await self.bot.fetch_channel(int(msg.reference.channel_id))
            ref_msg = await ref_ch.fetch_message(int(msg.reference.message_id))  
            ctt.append(f"┌ {ref_msg.author.display_name} ({msg.author}) {ref_msg.content}")
        
        ctt.append(f"{msg.author.display_name} ({msg.author})\n")

        if msg.attachments:
            ctt.append(f">> File(url=\"{msg.attachments[0].url}\")\n")
        elif msg.embeds:
            ctt.append(f">> Embed(image.url=\"{msg.embeds[0].image.url}\")\n")
        elif msg.stickers:
            ctt.append(f">> Sticker()\n")
        elif msg.content:
            ctt.append(f">> {msg.content}\n")
        else:
            ctt.append('"Nothing"\n')

        ctt.append("```")
        
        return "".join(ctt)

def setup(bot):
    bot.add_cog(Log(bot))