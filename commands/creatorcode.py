import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class creatorcode(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="クリエイターコードを検索できる",
    usage="creatorcode [クリエイターコード]"
  )
  async def creatorcode(self,ctx,search=None):
    if search == None:
      embed=nextcord.Embed(title="クリエイターコードを入力してください",description="検索したいクリエイターコードを入力してください",color=color)
      await ctx.send(embed=embed)
    else:
      search = requests.get(f"https://fortnite-api.com/v2/creatorcode?name={search}").json()
      if search['status'] == 200:
        data = search['data']        
        embed=nextcord.Embed(title=data['code'],color=color)
        embed.add_field(name="アカウント名",value=data['account']['name'])
        if data['status'] == "ACTIVE":
          status = "アクティブ"
        elif data['status'] == "INACTIVE":
          status = "アクティブでない"
        elif data['status'] == "DISABLED":
          status = "無効化されている"
        else:
          status = "不明"
        embed.add_field(name="コードの状態",value=status)
        await ctx.send(embed=embed)
      elif search['status'] == 404:
        embed=nextcord.Embed(title="見つかりませんでした",description="クリエイターコードが見つかりませんでした",color=color)
        await ctx.send(embed=embed)
          
def setup(bot):
  return bot.add_cog(creatorcode(bot))