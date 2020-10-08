
import discord
import os
import os.path
import json

import asyncio


def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname

class Bot(object):
    def __init__(self):
        self.client = discord.Client()

    def run(self):
            
        async def runner(*args, **kwargs):
            try:
                await self.client.start(*args, **kwargs)
            finally:
                if not self.client.is_closed():
                    await self.client.close()

        
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
            asyncio.run(runner(token))
        
    async def get_user_by_id(self, user_id):
        return await self.client.get_user(381870129706958858)
    
    async def get_roles_of_user(self, user_id, guild_id):
        guild = await self.client.get_guild(guild_id)
        member = await guild.get_member(user_id)
        return member.roles

if __name__ == '__main__':
    b = Bot()
    b.run()
