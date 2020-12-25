import discord, os, requests, json, firebase_admin, asyncio
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

client = discord.Client()
now = datetime.now()
current_time = now.strftime("%Y-%m-%d-%H-%M-%S")
dab = firestore.client()
check = False

class BirthdayCheck(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("BirthdayCheck cog loaded")
    
    #Check for birthdays
    async def get_birthdays(self, ctx):
        try:
            ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            amount = len(ref) - 1
        except Exception as e:
            print(e)

    #Test
    @commands.command()
    async def test(self, ctx):
        print('Recieved: >test')
        print(current_time)
        await ctx.send('testing complete')
        print('Response: testing complete')
        print('----------')

    #Infinite Loop
    async def infinite_loop(self, ctx):
        await client.wait_until_ready()
        while not client.is_closed:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d-%H-%M-%S")
            try:
                if current_time == '2020-12-25-17-40-00':
                    channel = client.get_channel(754627439413690469)
                    await channel.send('Countdown has initialized <a:Loading:792062970599178251>')
                    await channel.send('3 More Days till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
                if current_time == '2020-12-26-17-40-00':
                    channel = client.get_channel(754627439413690469)
                    await channel.send('2 More Days till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
                if current_time == '2020-12-27-17-40-00':
                    channel = client.get_channel(754627439413690469)
                    await channel.send('1 More Day till a̶̧͔̱̰̩̋͑̅̾͗̈́̐͂̚͘g̸̺̣̟̜̓̓́́͘h̸͖͈̺̿̊͆͒̅̎̑̚ͅa̴̙̫̗̟͐͂̈̀̒̅͛̉͠s̴̺̔̌͑͑s̷̞̥͈͚̺͈͕̀̀͂̇́͘ͅȁ̵̬̀̂̂̎͝g̸͓̞̑̐̏̉́͆͝h̷̹̯̣͈̻̺͑̾́́̔͗̐̓͘k̸̯̟̼̮̜̏͐͜....')
            except Exception as e:
                print(e)
            await asyncio.sleep(60)
    
    client.loop.create_task(infinite_loop())

def setup(client):
    client.add_cog(BirthdayCheck(client))