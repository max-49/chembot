# chembot

If you're running this bot for some reason, add a `profiles.json` into the root directory and put `[]` in it. 
Also, make a file called `config.py` and put the following code into it:
```py
import os

def get_bot(cwd, debug=True):
  # returns bot token, NP game, currency, and prefix
  if(debug):
    return [os.getenv('TOKEN'), "developing!", "coins", "c!"]
  elif(cwd == 'chembot'):
    return [os.getenv('CHEM_TOKEN'), "with TeamlessCTF!", "coins", "c!"]
  else:
    # if your cwd's name is something other than chembot
```
also your first command when running the bot for the first time should be c!profile otherwise things might break

have fun
