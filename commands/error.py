import nextcord
from nextcord.ext import commands,tasks
import json
import requests
import io

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class error(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self,ctx,error:Exception):
    if isinstance(error,commands.errors.CommandNotFound):
      embed=nextcord.Embed(title="コマンドが見つかりません",description=f"コマンドが見つかりませんでした\n`{config['prefix']}help`でコマンドを確認してください",color=color)
      await ctx.send(embed=embed)
    elif isinstance(error,commands.errors.NotOwner):
      embed=nextcord.Embed(title="このコマンドは実行できません",description=f"このコマンドはBot作成者以外実行できません",color=color)
      await ctx.send(embed=embed)

def setup(bot):
  return bot.add_cog(error(bot))
