import nextcord
from nextcord.ext import commands
import json
import requests

from modules import updater

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class check_update(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.is_owner()
  @commands.command(
    description="Botのアップデートがあるか確認できる",
    usage="check_update"
  )
  async def check_update(self,ctx):
    embed=updater.command_check_updater()
    await ctx.send(embed=embed)    

def setup(bot):
  return bot.add_cog(check_update(bot))
