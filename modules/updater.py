import json
import os
import requests
from replit import db
from colorama import Fore

def updater():
  with open('config.json','r') as f:
    config = json.load(f)
  with open('bot.json','r') as f:
    bot = json.load(f)

  version = bot['version']  
  git = f"{bot['git_raw']}/{bot['git_branch']}"
  new_version = requests.get(f"{git}/bot.json").json()['version']
  if version != new_version:
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートを確認しました\nアップデートを実行します" + Fore.RESET)
    files = os.listdir("modules")
    for file in files:
      if file.startswith("_"):
        continue
      new_file = requests.get(f"{git}/modules/{file}").text
      with open(f'modules/{file}','w') as f:
        f.write(new_file)
    new_config = requests.get(f"{git}/config.json").json()
    for key in config:
      db[key] = str(config[key])
    with open('config.json','w') as f:
      json.dump(new_config,f,indent=2)
    for key in db.keys():
      with open('config.json','r') as f:
        config = json.load(f)
        config[key] = str(db[key])
        del db[key]
      with open('config.json','w') as f:
        json.dump(config,f,indent=2)
    with open('bot.json','r') as f:     
      bot = json.load(f)
      bot['version'] = new_version
    with open('bot.json','w') as f:
      json.dump(bot,f,indent=2)    
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートが正常に完了しました" + Fore.RESET)    
