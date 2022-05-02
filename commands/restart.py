
import nextcord
from nextcord.ext import commands
import json
import requests
import os
import sys

from modules import updater

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class restart(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.is_owner()
  @commands.command(
    description="Botを再起動できる",
    usage="restart"
  )
  async def check_update(self,ctx):
    embed=nextcord.Embed(title="再起動",description="Botの再起動を実行します")
    await ctx.send(embed=embed)    
    os.execl(sys.executable,sys.executable,*sys.argv)
 
def setup(bot):
  return bot.add_cog(restart(bot))
