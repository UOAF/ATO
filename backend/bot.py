
import discord
import os
import os.path
import json
from cachetools import LRUCache, cached

import asyncio

def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname

class Bot(object):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.client = discord.Client()

    async def run(self):        
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
            await self.client.start(token)
            
    def get_user_by_id(self, user_id):
        return self.client.get_user(user_id)
    
    @cached(cache=LRUCache(maxsize=100))
    def get_roles_of_user(self, user_id):
        guild = self.client.get_guild(self.guild_id)
        member = guild.get_member(user_id)
        return member.roles
    
    def get_all_users(self):
        guild = self.client.get_guild(self.guild_id)
        return guild.members

if __name__ == '__main__':
    b = Bot()
    b.run()
