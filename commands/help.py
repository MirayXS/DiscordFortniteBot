import nextcord
from nextcord.ext import commands
import json
import requests

with open('config.json','r') as f:
  config = json.load(f)

with open('bots.json','r') as f:
  bots = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class invite_button(nextcord.ui.View):
  def __init__(self,id):
    super().__init__(timeout=None)
    self.value = None
    self.id = id    
    self.add_item(nextcord.ui.Button(label="Botを招待",url=f"https://discord.com/api/oauth2/authorize?client_id={self.id}&permissions=8&scope=bot"))
                  
class help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description="コマンド一覧,コマンドの詳細を見ることができる",
    usage="help [コマンド名,None]"
  )
  async def help(self,ctx,*,search=None):
    if search == None:
      command_list = []
      for command in self.bot.commands:
        command_list.append(command.name)
      embed=nextcord.Embed(description=' '.join(f"`{x}`" for x in command_list),color=color)
      embed.add_field(name="Github",value=f"[DiscordFortniteBot]({bots['github']})")      
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.display_avatar)
      embed.set_footer(text=f"コマンドの使い方は {config['prefix']}help [コマンド名] で確認できます")      
      await ctx.send(embed=embed,view=invite_button(self.bot.user.id))      
    else:
      command = self.bot.get_command(search.lower())
      if command == None:
        embed=nextcord.Embed(title="見つかりませんでした",description=f"コマンドが見つかりませんでした\n`{config['prefix']}help`でコマンドを確認してください",color=color)
        await ctx.send(embed=embed)
      else:
        embed=nextcord.Embed(title=f"{command.name}の詳細",description=command.description,color=color)
        embed.add_field(name="使い方",value=command.usage)        
        embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.display_avatar)
        await ctx.send(embed=embed)

def setup(bot):
  return bot.add_cog(help(bot))