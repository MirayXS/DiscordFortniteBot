import nextcord
from nextcord.ext import commands
import os
import sys
import traceback
import platform
import json
from colorama import Fore
from modules import updater

updater.updater()
with open('config.json','r') as f:
  config = json.load(f)
with open('bots.json','r') as f:
  bots = json.load(f)  

if config['token'] == "":
  print(Fore.RED + "Botのトークンを入力してください" + Fore.RESET)
  sys.exit(1)

bot = commands.Bot(
  command_prefix=config['prefix'],
  help_command=None,
  case_insensitive=True,
  intents = nextcord.Intents.all()  
)

@bot.event
async def on_ready():
  print(Fore.GREEN + f"DiscordFortniteBot:{bots['version']}\nPython:{platform.python_version()}\nnextcord:{nextcord.__version__}\nBot:{bot.user}\nBotが起動しました" + Fore.RESET)
  for extension in os.listdir("commands"):
    if extension.startswith("_"):
      continue
    try:
      bot.load_extension(f"commands.{extension.replace('.py','')}")
      print(Fore.BLUE + f"{extension}を読み込みました" + Fore.RESET)
    except:
      print(Fore.RED + f"{extension}を読み込めませんでした\n{traceback.format_exc()}" + Fore.RESET)
  presence = config['presence'].format(prefix=config['prefix'],server=len(bot.guilds))      
  await bot.change_presence(activity=nextcord.Game(name=presence))    
  if config['shop_channel'] == "":
    print(Fore.YELLOW + "ショップチャンネルが設定されていません" + Fore.RESET)  
try:
  bot.run(config['token'])
except nextcord.errors.PrivilegedIntentsRequired:
  print(Fore.RED + "Botのインテントが無効になっています\n下記URLから有効化してください\nhttps://discord.com/developers/applications\nわからない場合は\nhttps://github.com/p-yttor4869/DiscordFortniteBot/blob/main/docs/intents.md\nを参考にしてみてください")
