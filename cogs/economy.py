import discord
import logging
from discord.ext import commands
from discord.utils import get
from firebase_admin import firestore

dab = firestore.client()

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["s"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shop(self, ctx):
        logging.info('Recieved: >shop') 
        embed = discord.Embed(
            title="Shop",
            description="Come and see, come and see! We have more then enough scams for you!",
            color=0xff0000)
        embed.add_field(name="<:PixelGun:806977728094928906> Gun", value='1000 Scuffed Coins\n ID: gun', inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS and carried by Sirspam")
        await ctx.send(embed=embed)
        logging.info('Response: shop embed\n----------')
    
    @shop.group(aliases=["gun"])
    async def shop_gun(self, ctx):
        embed = discord.Embed(
            title="<:PixelGun:806977728094928906> Gun",
            description="Are we in texas or something?",
            color=0xff0000)
        embed.add_field(name="Buyable", value='Yes', inline=False)
        embed.add_field(name="Cost", value='1000 Scuffed Coins', inline=False)
        embed.add_field(name="Usable", value='Yes', inline=False)
        embed.add_field(name="Consumable", value='Yes', inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS and carried by Sirspam")
        await ctx.send(embed=embed)
        logging.info('Response: shop embed\n----------')
    
    @shop.group()
    async def buy(self, ctx):
        return #put some message here or something :)
        
    @buy.command(aliases=["gun"])
    async def buy_gun(self, ctx):
        inv = dab.collection('users').document(str(ctx.author.id)).get().get('inv')
        bal = dab.collection('users').document(str(ctx.author.id)).get().get('bal')
        inv_len = len(inv)
        a = 0
        while a < inv_len:
            item = str(inv[a]).split('~')
            if item[0] == 'gun':
                if bal > '1000':
                    count = int(item[1]) + 1
                    inv[a] = f'gun~{count}'
                    bal = bal - 1000
                    dab.collection('users').document(str(ctx.author.id)).update({'inv': inv, 'bal': bal})
                    await ctx.send(f'Gun has been added to your inv, you now own {count} guns')
                    logging.info('Response: Gun has been bought\n----------')
                else:
                    await ctx.send(f'I didnt know you where poor master OwO, you need at least 100 coins, you only have {bal}')
            a = a + 1
        
def setup(client):
    client.add_cog(economy(client))