import nextcord
from nextcord.ext import commands,tasks
import json
import asyncio
import requests
import io

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class auto_shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.shop_check.start()    

  @tasks.loop(minutes=5)
  async def shop_check(self):
    if config['shop_channel'] == "":
      self.shop_check.stop()
      return
    with open('bot/shop_hash.txt','r') as f:
      shop_hash = f.read()
    new_shop_hash = requests.get("https://api.nitestats.com/v1/shop/shophash").text
    if shop_hash != new_shop_hash:
      await asyncio.sleep(120)
      channel = self.bot.get_channel(int(config['shop_channel']))      
      image = requests.get("https://api.nitestats.com/v1/shop/image").content
      embed=nextcord.Embed(title="アイテムショップ",color=color)
      embed.set_image(url="attachment://shop.png")
      await channel.send(embed=embed,file=nextcord.File(fp=io.BytesIO(image), filename="shop.png"))
      with open('bot/shop_hash.txt','w') as f:
        f.write(new_shop_hash)        
      
def setup(bot):
  return bot.add_cog(auto_shop(bot))
