import discord, os, json, requests
from discord.ext import commands, tasks
from discord.utils import get

#Get Random Quote
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = (f"{json_data[0]['q']} - {json_data[0]['a']}")
    return(quote)

class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Text cog loaded")

    #Commands List
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author == self.client.user:
            return
    
    #ping
    @commands.command()
    async def ping(self, ctx):
        print('Recieved: >ping')
        await ctx.send(f'uwu *notices your ping* <w< ``{round(self.client.latency * 1000)}ms``')
        print(f'Response: {round(self.client.latency * 1000)}')
        print('----------')

    @commands.command(aliases=["no"]) #Keep this out of the help embed ;)
    @commands.cooldown(1, 120, commands.BucketType.guild)
    async def nope(self, ctx):
        print("Recieved >nope")
        await ctx.send("Join the NOPE clan <:GunChamp:796047943966523432>\nhttps://discord.gg/xH7AGnGXkf")
        print ("Response: Certainly not a link to the NOPE discord")
        print('----------')
    
    #Quote
    @commands.command()
    async def quote(self, ctx):
        print('Recieved: >quote')
        final = get_quote()
        await ctx.send(final)
        print(f'Response: {final}')
        print('----------')
    
    #Help
    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):
        print('Recieved: >help ')
        embed=discord.Embed(title="Help", url="https://www.youtube.com/watch?v=7LnQRFh_knk", description="You can find all kinds of commands here, most of them are probably broken", color=0xff0000)
        embed.set_author(name="Thijnmens", url="https://github.com/thijnmens/", icon_url="https://cdn.discordapp.com/avatars/490534335884165121/eaeff60636ebf53040d8d5c0761c6c67.png?size=256")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/790189114711605260/c6e486bab141b997eeceb42ac5c9a3c2.png?size=256")
        embed.add_field(name=">help", value="this fancy page", inline=False)
        embed.add_field(name=">user [mention]", value="get the info of a user", inline=False)
        embed.add_field(name=">user add", value="add yourself to the userbase. If you don't want to fill something in, please use ``None``", inline=False)
        embed.add_field(name=">user update <field> <new value>", value="Update your info, use ``>help update`` for the fields and more info!", inline=False)
        embed.add_field(name=">user remove", value="Removes your info from the database", inline=False)
        embed.add_field(name=">scoresaber [mention]", value="gets a user's ScoreSaber data,", inline=False)
        embed.add_field(name=">scoresaber topsong [mention]", value="gets a user's top song from ScoreSaber,", inline=False)
        embed.add_field(name=">scoresaber recentsong [mention]", value="gets a user's most recent song from ScoreSaber,", inline=False)
        embed.add_field(name=">challonge", value="Posts an embed of previous scuffed tournaments.", inline=False)
        embed.add_field(name=">quote", value="Posts a random quote", inline=False)
        embed.add_field(name=">ping", value="Pings Scuffed Bot", inline=False)
        embed.set_footer(text="this code was ruined by ThiJNmEnS#6059")
        await ctx.send(embed=embed)
        print('Response: help embed')
        print('----------')

    @help.command()
    async def update(self, ctx):
        embed=discord.Embed(title="Help User Update", color=0xff0000)
        embed.add_field(name="Username <value>", value="Updates your username.\nYou can put anything here, so go nuts", inline=False)
        embed.add_field(name="Scoresaber <value>", value="Updates your Scoresaber.\nUse a valid scoresaber link, otherwise the scoresaber command won't work!", inline=False)
        message = ""
        for x in self.client.valid_HMD:
            message = message+x+", "
        embed.add_field(name="HMD <value>", value=f"Updates your Head Mounted Display.\nValid values are: ``{message}``", inline=False)
        embed.add_field(name="Birthday <values>", value="Updates your birthday.\nOnly the format of DD/MM or DD/MM/YYYY will be accepted", inline=False)
        embed.add_field(name="Status <values>", value="Updates your status.\nYou can put anything here, so go nuts", inline=False)
        #embed.add_field(name="Colour", value="", inline=True) I'll add this once I actually get it working :pepelaff:
        await ctx.send(embed=embed)

def setup(client):    
    client.add_cog(Text(client))