
import discord
import os
import os.path
import json

client = discord.Client()


def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname

client = discord.Client()


if __name__ == '__main__':
    configfile = os.path.join(get_mod_path(), 'bot_config.json')
    if not os.path.exists(configfile):
        print("Config file not found, please enter your auth token here:")
        token = input('--> ')
        token = token.strip()
        with open(configfile, 'w') as jsonconfig:
            json.dump({'token': token}, jsonconfig)

    with open(configfile, 'r') as jsonconfig:
        config = json.load(jsonconfig)
        token = config['token']
        if token == 'YOUR_TOKEN_HERE':
            raise ValueError("You must set a token in config.json.")
    client.run(token)

