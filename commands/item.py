import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class item(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="アイテムを検索できる",
    usage="item [アイテム名]"
  )
  async def item(self,ctx,search=None):
    if search == None:
      embed=nextcord.Embed(title="アイテム名を入力してください",description="検索したいアイテム名を入力してください",color=color)
      await ctx.send(embed=embed)
    else:
      count = 0      
      name_search = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search/all?name={search}&matchMethod=starts&language=ja&searchLanguage=ja").json()
      if name_search["status"] == 200:  
        for item in name_search['data']:
          embed=nextcord.Embed(title=item['name'],description=item['description'],color=color)
          embed.add_field(name="ID",value=item['id'])
          embed.add_field(name="レアリティ",value=item["rarity"]["displayValue"])     
          if item["images"]["icon"] != None:
            embed.set_thumbnail(url=item["images"]["icon"])
          await ctx.send(embed=embed)
          count += 1
          if count == int(config['search_max']):
            embed=nextcord.Embed(title="検索最大数に到達しました",description="アイテムの検索最大数に到達しました",color=color)
            await ctx.send(embed=embed)
            return       
      elif name_search["status"] == 404:
        id_search = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search/all?id={search}&matchMethod=starts&language=ja&searchLanguage=ja").json()
        if id_search["status"] == 200:
          for item in id_search['data']:
            embed=nextcord.Embed(title=item['name'],description=item['description'],color=color)
            embed.add_field(name="ID",value=item['id'])
            embed.add_field(name="レアリティ",value=item["rarity"]["displayValue"])     
            if item["images"]["icon"] != None:
              embed.set_thumbnail(url=item["images"]["icon"])
            await ctx.send(embed=embed)
            count += 1
            if count == int(config['search_max']):
              embed=nextcord.Embed(title="検索最大数に到達しました",description="アイテムの検索最大数に到達しました",color=color)
              await ctx.send(embed=embed)
              return
        elif id_search["status"] == 404:
          embed=nextcord.Embed(title="見つかりませんでした",description="アイテムが見つかりませんでした",color=color)
          await ctx.send(embed=embed)

def setup(bot):
  return bot.add_cog(item(bot))