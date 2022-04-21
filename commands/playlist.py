import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class playlist(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="プレイリストを検索できる",
    usage="playlist [プレイリスト名]"
  )
  async def playlist(self,ctx,search=None):
    if search == None:
      embed=nextcord.Embed(title="プレイリスト名を入力してください",description="検索したいプレイリスト名を入力してください",color=color)
      await ctx.send(embed=embed)
    else:
      count = 0      
      name_search = requests.get(f"https://tel1hor-fortniteapi.tel1hor.tk/playlist/search?name={search}").json()
      if name_search['status'] == 200:
        for playlist in name_search['data']:
          embed = nextcord.Embed(title=playlist['name'],description=playlist['description'],color=color)
          embed.add_field(name="ID", value=playlist['id'])
          embed.add_field(name="最大プレイヤー数",value=playlist['maxPlayers'])
          embed.add_field(name="最大チーム数",value=playlist['maxTeams'])
          if playlist['images']['showcase'] != None:
            embed.set_image(url=playlist['images']['showcase'])
          await ctx.send(embed=embed)
          count += 1
          if count == int(config['search_max']):
            embed=nextcord.Embed(title="検索最大数に到達しました",description="アイテムの検索最大数に到達しました",color=color)
            await ctx.send(embed=embed)
            return
      elif name_search['status'] == 404:
        id_search = requests.get(f"https://tel1hor-fortniteapi.tel1hor.tk/playlist/search?id={search}").json()
        if id_search['status'] == 200:
          for playlist in id_search['data']:
            embed = nextcord.Embed(title=playlist['name'],description=playlist['description'],color=color)
            embed.add_field(name="ID", value=playlist['id'])
            embed.add_field(name="最大プレイヤー数",value=playlist['maxPlayers'])
            embed.add_field(name="最大チーム数",value=playlist['maxTeams'])
            if playlist['images']['showcase'] != None:
              embed.set_image(url=playlist['images']['showcase'])
            await ctx.send(embed=embed)
            count += 1
            if count == int(config['search_max']):
              embed=nextcord.Embed(title="検索最大数に到達しました",description="アイテムの検索最大数に到達しました",color=color)
              await ctx.send(embed=embed)
              return
        elif id_search['status'] == 404:
          embed=nextcord.Embed(title="見つかりませんでした",description="プレイリストが見つかりませんでした",color=color)
          await ctx.send(embed=embed)

def setup(bot):
  return bot.add_cog(playlist(bot))