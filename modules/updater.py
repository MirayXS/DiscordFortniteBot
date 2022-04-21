import json
import os
import requests
from replit import db
from colorama import Fore

def updater():
  with open('config.json','r') as f:
    config = json.load(f)
  with open('bots.json','r') as f:
    bots = json.load(f)

  version = bots['version']  
  git = f"{bots['git_raw']}/{bots['git_branch']}"
  new_version = requests.get(f"{git}/bots.json").json()['version']
  if version != new_version:
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートを確認しました\nアップデートを実行します" + Fore.RESET)   
    for file in os.listdir("modules"):
      if file.startswith("_"):
        continue
      new_file = requests.get(f"{git}/modules/{file}").text
      with open(f'modules/{file}','w') as f:
        f.write(new_file)
    for file in os.listdir("commands"):
      if file.startswith("_"):
        continue
      new_file = requests.get(f"{git}/commands/{file}").text
      with open(f'commands/{file}','w') as f:
        f.write(new_file)
    new_main = requests.get(f"{git}/main.py").text 
    with open('main.py','w') as f:
      f.write(new_main)
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
    with open('bots.json','r') as f:     
      bots = json.load(f)
      bots['version'] = new_version
    with open('bots.json','w') as f:
      json.dump(bots,f,indent=2)    
    print(Fore.GREEN + f"バージョン{new_version}へのアップデートが正常に完了しました" + Fore.RESET)
  else:
    print(Fore.GREEN + "アップデートは見つかりませんでした" + Fore.RESET)

