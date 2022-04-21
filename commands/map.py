import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class map(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="現在のバトルロワイヤルのマップを表示できる",
    usage="map"
  )
  async def map(self,ctx):
    map = requests.get("https://fortnite-api.com/v1/map?language=ja").json()['data']['images']['blank']
    embed=nextcord.Embed(title="バトルロワイヤルのマップ",color=color)
    embed.set_image(url=map)
    await ctx.send(embed=embed)    
    
def setup(bot):
  return bot.add_cog(map(bot))