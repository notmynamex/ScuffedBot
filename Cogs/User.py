import discord, os, requests, json, firebase_admin, asyncio, time, re
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()
valid_HMD = ["cv1","rift S","quest","quest 2","index","vive"]

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
        links_Message = ""
        ref = dab.collection(str(ctx.author.id)).document('data').get()
        username = ref.get("username")
        scoresaber = ref.get("scoresaber")
        links_Message = f"[Scoresaber]({scoresaber})"+links_Message
        birthday = ref.get("birthday")
        hmd = ref.get("hmd")
        try:
            twitch = ref.get("twitch")
            links_Message = links_Message+f" [Twitch]({twitch})"
        except Exception as e:
            print (f"funny twitch exception")
        try:
            colour = int(ref.get("colour"))
            embed=discord.Embed(title=username, colour=discord.Colour(colour))
        except Exception as e:
            embed=discord.Embed(title=username, colour=discord.Colour.random())
            print (f"Funny colour exception: {e}")
        embed.add_field(name="Links", value=links_Message, inline=False)
        embed.add_field(name="HMD", value=hmd, inline=True)
        embed.add_field(name="Birthday", value=birthday, inline=True)
        try:
            status = ref.get("status")
            embed.add_field(name="Status", value=status, inline=False)
        except Exception as e:
            print (f"Funny status exception: {e}")
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
                    scoresaber = scoresaber.split("?", 1)[0]
                    scoresaber = scoresaber.split("&", 1)[0]
                    print(scoresaber)
                    if msg:
                        sent = await ctx.send("When is your birthday? [DD/MM] or [DD/MM/YYYY].\nUse ``None`` if you don't want to input anything.")
                        try:
                            msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                            birthday = msg.content
                            print(birthday)
                            if birthday != "None":
                                if ((bool(re.search(r"\d/", birthday)))) is False:
                                    print ("Birthday input validation triggered")
                                    await ctx.send("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
                                    return
                                storer = birthday.split('/')
                                storer[0] = int(storer[0])
                                storer[1] = int(storer[1])
                                if(storer[1]>12 or storer[1]<1 or storer[0]>31 or storer[0]<1):
                                    print ("Birthday legitimacy triggered")
                                    await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate date``")
                                    return
                            a = False
                            if msg:
                                sent = await ctx.send("What headset do you use?")
                                try:
                                    msg = await self.client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                    hmd = msg.content
                                except Exception as e:
                                    print (e)
                                doc_ref = dab.collection(str(ctx.author.id)).document('data')
                                doc_ref.set({
                                    'a':a,
                                    'username':username,
                                    'scoresaber':scoresaber,
                                    'birthday':birthday,
                                    'hmd':hmd})
                                try:
                                    col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
                                    col_ref.append(str(ctx.author.id))
                                    dab.collection('collectionlist').document('data').update({
                                        'collectionarray':col_ref})
                                except Exception as e:
                                    print(e)
                            await ctx.send(f'{ctx.author.name} has sucessfully been added to the database!\nUse ``>user update`` to add optional customisation')
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
        try:
            col_ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
            col_ref.remove(str(ctx.author.id))
            dab.collection('collectionlist').document('data').get
            await ctx.send(f"{ctx.author.name} has been successfully removed from the database")
            print(f"Response: {ctx.author.id} has been successfully removed to the database")
            print('----------')
        except Exception as e:
            print(e)
                
    #User update
    @user.group(invoke_without_command=True, case_insensitive=True)
    async def update(self, ctx):
        print(f"Recieved: >user update")
        await ctx.send("B-Baka!! You need to tell me what you want to update!!\nUse ``>user update help`` to check the valid arguments")
        print("no sub command given")
        print("---------")
        
    @update.command()
    async def username(self, ctx, *, argument):
        print(f'Recieved: >user update username {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'username':argument})
        await ctx.send(f"Your username has been updated to {argument}")
        print(f"{ctx.author.name} has updated their username to {argument}")
        print('----------')
    
    @update.command()
    async def birthday(self, ctx, argument):
        print(f'Recieved: >user update birthday {ctx.author.name}')
        if ((bool(re.search(r"\d/", argument)))) is False:
            print ("Birthday input validation triggered")
            await ctx.send("Oopsie, looks like you did a woopsie! uwu\n``Don't use characters expect for numbers and /``")
            return
        storer = argument.split('/')
        storer[0] = int(storer[0])
        storer[1] = int(storer[1])
        if(storer[1]>12 or storer[1]<1 or storer[0]>31 or storer[0]<1):
            print ("Birthday legitimacy triggered")
            return await ctx.send("B-Baka!! that date doesn't make any sense!\n``Please use a legitimate date``")
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'birthday':argument})
        await ctx.send(f"Your birthday has been updated to {argument}")
        print(f"{ctx.author.name} has updated their birthday to {argument}")
        print('----------')
    
    @update.command()
    async def hmd(self, ctx, *, argument):
        print(f'Recieved: >user update hmd {ctx.author.name}')
        if argument not in valid_HMD:
            print (f"{argument} not in valid_HMD")
            return await ctx.send("BAKA!! That HMD isn't valid!\n``Use >user update help to check the valid HMDs``")
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'hmd':argument})
        await ctx.send(f"Your hmd has been updated to {argument}")
        print(f"{ctx.author.name} has updated their status to {argument}")
        print('----------')
    
    @update.command()
    async def status(self, ctx, *, argument):
        print(f'Recieved: >user update status {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'status':argument})
        await ctx.send("Your status has been updated")
        print(f"{ctx.author.name} has updated their status to {argument}")
        print('----------')
    
    @update.command(aliases=["color"]) #Americans ew
    async def colour(self, ctx, argument):
        print(f"Recieved: >user update colour {ctx.author.name}")
        if len(argument) != 6:
            await ctx.send("Please use a valid hexadecimal colour value. uwu")
        else:
            doc_ref = dab.collection(str(ctx.author.id)).document('data')
            doc_ref.update({
                'colour':argument})
            await ctx.send("Your colour has been updated")
            print(f"{ctx.author.name} has updated their colour to {argument}")
            print('----------')

    @update.command()
    async def help(self, ctx):
        embed=discord.Embed(title="User update help", color=0xff0000)
        embed.add_field(name="Username", value="", inline=True)
        embed.add_field(name="Scoresaber", value="", inline=True)
        embed.add_field(name="HMD", value="", inline=True)
        embed.add_field(name="Birthday", value="", inline=True)
        embed.add_field(name="Status", value="", inline=True)
        #embed.add_field(name="Colour", value="", inline=True) I'll add this once I actually get it working :pepelaff:
        await ctx.send(embed=embed)

    @update.group(invoke_without_command=True, case_insensitive=True)
    async def link(self, ctx):
        await ctx.send("``Scoresaber, Twitch``")

    @link.command()
    async def scoresaber(self, ctx, argument):
        print(f'Recieved: >user update link scoresaber {ctx.author.name}')
        argument = argument.split("?", 1)[0]
        argument = argument.split("&", 1)[0]
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'scoresaber':argument})
        await ctx.send("Your scoresaber has been updated")
        print(f"{ctx.author.name} has updated their scoresaber to {argument}")
        print('----------')

    @link.command()
    async def twitch(self, ctx, argument):
        print(f'Recieved: >user update link twitch {ctx.author.name}')
        doc_ref = dab.collection(str(ctx.author.id)).document('data')
        doc_ref.update({
            'twitch':argument})
        await ctx.send("Your twich has been updated")
        print(f"{ctx.author.name} has updated their twitch to {argument}")
        print('----------')

def setup(client):    
    client.add_cog(User(client))
