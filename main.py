import os
import sys
import platform
import json
from colorama import Fore
from modules import updater
try:
  import nextcord
  from nextcord.ext import commands
except ModuleNotFoundError:
  print(Fore.RED + "ライブラリの読み込みに失敗しました\nインストールを実行します" + Fore.RESET)
  os.system("pip install -r bot/requirements.txt") 
  os.system("clear")
  print(Fore.GREEN + "ライブラリのインストールが完了しました\nもう一度起動してください" + Fore.RESET)
  sys.exit(1)  

updater.updater()
with open('config.json','r') as f:
  config = json.load(f)
with open('bots.json','r') as f:
  bots = json.load(f)  

if config['token'] == "":
  print(Fore.RED + "Botのトークンを入力してください" + Fore.RESET)
  sys.exit(1)
  
bot = commands.Bot(command_prefix=config['prefix'])

@bot.event
async def on_ready():
  print(Fore.GREEN + f"DiscordFortniteBot:{bots['version']}\nPython:{platform.python_version()}\nnextcord:{nextcord.__version__}\nBot:{bot.user}\nBotが起動しました" + Fore.RESET)
  
bot.run(config['token'])
