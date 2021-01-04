import discord, os, requests, json, firebase_admin, asyncio, schedule, time
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("User cog loaded")

    #User
    @commands.group(invoke_without_command=True)
    async def user(self, ctx, argument=None):
        if argument is not None:
            ID = argument[3:]
            ID = ID[:-1]
            ctx.author = self.client.get_user(int(ID))
        print(f'Recieved: >user {ctx.author.name}')
        ref = dab.collection(str(ctx.author.id)).document('data').get()
        username = ref.get('username')
        scoresaber = ref.get('scoresaber')
        birthday = ref.get('birthday')
        embed=discord.Embed(title=username, color=0xff0000)
        embed.add_field(name="Scoresaber", value=scoresaber, inline=False)
        embed.add_field(name="Birthday", value=birthday, inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        print('Response: user embed')
        print('----------')
        
    #User Add
    @user.command()
    async def add (self, ctx):
        print(f'Recieved: >user add {ctx.author.name}')
        sent = await ctx.send('How would you like to be called?')
        try:
            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            username = msg.content
            print(username)
            if msg:
                sent = await ctx.send('What is your scoresaber link?')
                try:
                    msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                    scoresaber = msg.content
                    print(scoresaber)
                    if msg:
                        sent = await ctx.send('When is your birthday? [DD/MM/YYYY]')
                        try:
                            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                            birthday = msg.content
                            print(birthday)
                            doc_ref = dab.collection(str(ctx.author.id)).document('data')
                            doc_ref.set({
                                'username':username,
                                'scoresaber':scoresaber,
                                'birthday':birthday})
                            try:
                                col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
                                col_ref.append(str(ctx.author.id))
                                col_ref.update({
                                    'collectionarray':col_ref})
                            except Exception as e:
                                print(e)
                            await ctx.send(f'{ctx.author.name} has sucessfully been added to the database')
                            print(f'Response: {ctx.author.name} has sucessfully been added to the database')
                            print('----------')
                        except asyncio.TimeoutError:
                            await sent.delete()
                            await ctx.send('You did not reply in time, please restart the process')
                except asyncio.TimeoutError:
                    await sent.delete()
                    await ctx.send('You did not reply in time, please restart the process')
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('You did not reply in time, please restart the process')

                
    #User Remove
    @user.command()
    async def remove(self, ctx):
        dab.collection(str(ctx.author.id)).document('data').delete()
        await ctx.send(f"{ctx.author.name} has been successfully removed from the database")
        print(f"Response: {ctx.author.id} has been successfully removed to the database")
        print('----------')
                
    #User update
    @user.command()
    async def update(self, ctx, argument1=None, argument2=None):
        if(argument1 == 'username'):
            print(f'Recieved: >user update username {ctx.author.name}')
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.update({
                'username':argument2})
            await ctx.send("Your username has been updated")
            print(f"{ctx.author.name} has updated their username to {argument2}")
            print('----------')
        if(argument1 == 'scoresaber'):
            print(f'Recieved: >user update scoresaber {ctx.author.name}')
            sep = "?"
            stripped = argument2.split(sep, 1)[0]
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.update({
                'scoresaber':stripped})
            await ctx.send("Your scoresaber has been updated")
            print(f"{ctx.author.name} has updated their scoresaber to {stripped}")
            print('----------')
        if(argument1 == 'birthday'):
            print(f'Recieved: >user update birthday {ctx.author.name}')
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.update({
                'birthday':argument2})
            await ctx.send("Your birthday has been updated")
            print(f"{ctx.author.name} has updated their birthday to {argument2}")
            print('----------')
        if(argument1 is None):
            await ctx.send('Please include an option to change (username, scoresaber, birthday)')
            print('no argument1 given')
            print('----------')

def setup(client):    
    client.add_cog(User(client))