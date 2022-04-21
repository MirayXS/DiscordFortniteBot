import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class news(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="現在のバトルロワイヤルニュースを表示できる",
    usage="news"
  )
  async def news(self,ctx):
    news = requests.get("https://fortnite-api.com/v2/news/br?language=ja").json()['data']['image']
    embed=nextcord.Embed(title="バトルロワイヤルニュース",color=color)
    embed.set_image(url=news)
    await ctx.send(embed=embed)    
    
def setup(bot):
  return bot.add_cog(news(bot))