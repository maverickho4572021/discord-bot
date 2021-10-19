# import discord
import json
# import math
import os
# import requests

from discord import errors
from discord.ext import commands
# from discord_components import Button, DiscordComponents
# from discord_components.component import ButtonStyle
from fnmatch import fnmatch
from ext.tool import webhook_send
# from tqdm import tqdm


EXT_PATH = "./ext"
EMOJI_PATH = EXT_PATH + "/Emoji"
SOURCE_PATH = EMOJI_PATH + "/source"

GUILD_ID = 9876543210

MALE_COLOR = 0x5865f2
FEMALE_COLOR = 0xed4245

class Emoji():
    def __init__(self, a: str = "", name: str = "", id: str = "", path: str = ""):
        self.a=a
        self.name = name
        self.id = id
        self.source_path = path
        
    def __str__(self):
        return f"<{self.a}:{self.name}:{self.id}>"
        
    def __repr__(self):
        return f"<{self.a}:{self.name}:{self.id}>"

def get_emojis_info_from_msg(ctt):

    emojis = []
    while fnmatch(ctt, "*<:*:*>*") == True or fnmatch(ctt, "*<a:*:*>*") == True:
        tmp_emoji = Emoji()
        
        begin = ctt.index("<") + 1
        end = ctt.index(":", begin)
        tmp_emoji.a = ctt[begin:end]

        begin = end + 1
        end = ctt.index(":", begin)
        tmp_emoji.name = ctt[begin:end]
            
        begin = end + 1
        end = ctt.index(">", begin)
        tmp_emoji.id = ctt[begin:end]

        ctt = ctt[end:]
        emojis.append(tmp_emoji)

    return emojis

async def delete_message(bot, ch_id, msg_id):
    ch = await bot.fetch_channel(ch_id)
    try:
        msg = await ch.fetch_message(msg_id)
        await msg.delete()
    except errors.NotFound:
        pass

class EmojiSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_dict = None
        self.webhook_dict = {}

    async def load_emojis(self):
        # Custom Emoji
        # > Load emoji from ./ext/Emoji/source

        custom_emojis = {}

        for cate in os.listdir(SOURCE_PATH):
            sub_emojis = {}

            for file_name in os.listdir(f"{SOURCE_PATH}/{cate}"):

                emoji_name = file_name[:-4]

                sub_emojis[emoji_name] = Emoji(
                    a="a" if file_name[-4:] == ".gif" else "",
                    name=emoji_name,
                    path=f"{SOURCE_PATH}/{cate}/{file_name}"
                )
           
            custom_emojis[cate] = sub_emojis


        # Guild Emoji
        # > Load emoji data from ./ext/Emoji/__guild_emoji__.json

        guild_emojis = {}

        with open(f"{EMOJI_PATH}/__guild_emoji__.json", mode="r", encoding="utf8") as json_file:
            list_dict = json.load(json_file)
        
        for cate in list_dict:
            sub_emojis = {}

            for emoji in list_dict[cate]:
                emoji_info = emoji[1:-1].split(":")

                sub_emojis[emoji_info[1]] = Emoji(
                    a=emoji_info[0],
                    name=emoji_info[1],
                    id=emoji_info[2]
                )
            
            guild_emojis[cate] = sub_emojis

        self.emoji_dict = {}
        self.emoji_dict["custom"] = custom_emojis
        self.emoji_dict["guild"] = guild_emojis

    async def load_webhooks(self):

        for guild in self.bot.guilds:
            for ch in guild.text_channels:

                webhooks = await ch.webhooks()
                if not webhooks:
                    wh = await ch.create_webhook(name="Captain Hook")
                    self.webhook_dict[ch.id] = wh.url
                else:
                    self.webhook_dict[ch.id] = webhooks[0].url

    def save_guild_emojis(self):
        
        list_dict = {}

        for cate in self.emoji_dict["guild"]:
            list_dict[cate] = []
            for emoji in self.emoji_dict["guild"][cate]:
                list_dict[cate].append(str(self.emoji_dict["guild"][cate][emoji]))
        
        with open(f"{EMOJI_PATH}/__guild_emoji__.json", mode="w", encoding="utf8") as json_file:
            json.dump(list_dict, json_file, ensure_ascii=False)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.emoji_dict == None:
            await self.load_data()
        
    @commands.Cog.listener()
    async def load_data(self):

        guild = self.bot.get_guild(GUILD_ID)
        emojis = [await guild.fetch_emoji(emoji.id) for emoji in guild.emojis]
        for emoji in emojis:
            if emoji.user.bot: await emoji.delete() 
        await self.load_emojis()
        await self.load_webhooks()
        
        print(f"Emoji extension is ready.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "<a:loading:866600939234132018>" and user == self.bot.user:

            if self.emoji_dict == None:
                await self.load_data()
                await reaction.message.clear_reactions()
                await reaction.message.add_reaction("🆗")          

    @commands.Cog.listener()
    async def on_message(self, msg):
        ctt = msg.content

        # get emoji from message
        if fnmatch(ctt, "*<:*:*>*") == True or fnmatch(ctt, "*<a:*:*>*") == True and msg.webhook_id == None:
            emoji_list = get_emojis_info_from_msg(ctt)
            
            for emoji in emoji_list:
                try:
                    guild = self.bot.get_emoji(int(emoji.id)).guild
                except:
                    return
 
                if guild.id != GUILD_ID and any(emoji.name in self.emoji_dict["guild"][cate] for cate in self.emoji_dict["guild"]) == False:
                    if str(guild) not in self.emoji_dict["guild"]:
                        self.emoji_dict["guild"][str(guild)] = {}
                    self.emoji_dict["guild"][str(guild)][emoji.name] = emoji
            self.save_guild_emojis()

        # change txt to emoji
        elif fnmatch(ctt, "*:*:*") == True and msg.author != self.bot.user and msg.webhook_id == None:
            
            ctt_list = ctt.split(":")
            for i in range(1, len(ctt_list), 2):

                # if emoji in guild dictionary
                result_list = [values.get(ctt_list[i]) for values in self.emoji_dict["guild"].values() if values.get(ctt_list[i])]

                if result_list:
                    ctt_list[i] = str(result_list[0])
                    continue


                # if emoji in Bot Test Guild
                if any(ctt_list[i] == emoji.name for emoji in self.bot.get_guild(GUILD_ID).emojis):
                    result_list = [emoji for emoji in self.bot.get_guild(GUILD_ID).emojis if ctt_list[i] == emoji.name]
                    ctt_list[i] = str(result_list[0])
                    continue

                # if emoji in custom dictionary
                result_list = [values.get(ctt_list[i]) for values in self.emoji_dict["custom"].values() if values.get(ctt_list[i])]
                
                if result_list:
                    emoji = result_list[0]
                    with open(f"{emoji.source_path}", "rb") as file:
                        try:
                            emoji = await self.bot.get_guild(GUILD_ID).create_custom_emoji(
                                    name=ctt_list[i],
                                    image=bytearray(file.read())
                                )
                            ctt_list[i] = str(emoji)
                            continue
                        except errors.HTTPException:
                            await msg.channel.send(f"<@636841015700881411> :{ctt_list[i]}: 檔案有問題")
               
                # emoji not in dictionary
                ctt_list[i] = f":{ctt_list[i]}:"

            new_ctt = "".join(ctt_list)

            if new_ctt != ctt: 
                await msg.delete()
                await webhook_send(
                    url=self.webhook_dict[msg.channel.id],
                    content=new_ctt,
                    username=msg.author.display_name,
                    avatar_url=msg.author.avatar_url
                )
    
def setup(bot):
    bot.add_cog(EmojiSys(bot))