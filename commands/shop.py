import nextcord
from nextcord.ext import commands
import json
import requests
import io

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="現在のデイリーショップを見ることができる",
    usage="shop"
  )
  async def shop(self,ctx):
    embed=nextcord.Embed(title="取得中です",description="ショップ画像を取得中です",color=color)
    message = await ctx.send(embed=embed)
    image = requests.get("https://api.nitestats.com/v1/shop/image").content
    embed=nextcord.Embed(title="アイテムショップ",color=color)
    embed.set_image(url="attachment://shop.png")
    await message.edit(embed=embed,file=nextcord.File(fp=io.BytesIO(image), filename="shop.png"))

def setup(bot):
  return bot.add_cog(shop(bot))