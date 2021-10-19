from discord.ext import commands
from discord.user import ClientUser, User
from fnmatch import fnmatch
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # chrome_options = Options()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        # self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.get("https://www.google.com/imghp?sbi=1")


    @commands.Cog.listener()
    async def on_message(self, msg):
        avatar_id = None
        
        if msg.content[:7] == "avatar " or msg.content[:7] == "search ":
            name = msg.content[7:]
            members = [member for member in msg.guild.members]
            for member in members:
                if fnmatch(str(member.nick), f"*{name}*") or fnmatch(str(member.name), f"*{name}*"):
                    avatar_id = member.id
                    break

            if avatar_id and (type(self.bot.get_user(int(avatar_id))) == User or type(self.bot.get_user(int(avatar_id))) == ClientUser):
                if msg.content[:7] == "search ":
                    # search = self.driver.find_element_by_name("image_url")
                    # print(self.bot.get_user(int(avatar_id)).avatar_url)
                    # search.send_keys(str(self.bot.get_user(int(avatar_id)).avatar_url))
                    # search.send_keys(Keys.RETURN)
                    # await msg.channel.send(self.driver.current_url)
                    # self.driver.get("https://www.google.com/imghp?sbi=1")
                    pass

                else:
                    if type(self.bot.get_user(int(avatar_id))) == User or type(self.bot.get_user(int(avatar_id))) == ClientUser:
                        await msg.channel.send(self.bot.get_user(int(avatar_id)).avatar_url)

            else:
                await msg.channel.send("沒有暱稱或使用者名稱包含這個字詞的用戶")


def setup(bot):
    bot.add_cog(Avatar(bot))