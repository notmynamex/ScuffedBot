import logging
from discord.ext import commands
from random import getrandbits, choice, randint


lobby_vc_id = int(764546987441258506) # tourney time vc
coord_roles_ids = [785420213801582593, 785420338673614848, 785420354440921109, 775663293695524905] # owner perms, admin perms, mod perms, coordinator
ignored_roles = ["810492978816090173"] #spectator


class Coord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["coord","c"])
    @commands.has_any_role(*coord_roles_ids)
    async def coordinator(self, ctx):
        await ctx.send("Hi coordinator-kun ^w^")
    
    
    @coordinator.command(aliases=["m"], help="Mutes users in your vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def mute(self, ctx):
        logging.info("mute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Muting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        await member.edit(mute=True, deafen=True)
                        logging.info(f"{x.name} muted")
            else:
                await member.edit(mute=True, deafen=True)
                logging.info(f"{x.name} muted")
        await ctx.message.delete()
        logging.info("Finished muting\n-------------")



    @coordinator.command(aliases=["um"], help="Unmutes users in your vc.") #haha cum funny
    @commands.has_any_role(*coord_roles_ids)
    async def unmute(self, ctx):
        logging.info("Unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Unmuting in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.mute is True:
                await member.edit(mute=False, deafen=False)
                logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting\n-------------")
    

    @coordinator.command(aliases=["out"], help="Moves users to the lobby vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def move_out(self, ctx):
        logging.info("Move_in ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        await member.move_to(self.bot.get_channel(lobby_vc_id))
                        logging.info(f"{x.name} moved")
            else:
                await member.move_to(self.bot.get_channel(lobby_vc_id))
                logging.info(f"{x.name} moved")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")


    @coordinator.command(aliases=["in"], help="Moves mentioned users to your vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def move_in(self, ctx, *, argument):
        logging.info("Move_in ran")
        victims = argument.split() # I thought "victims" was a funny variable name for the users being moved :)
        for x in victims:
            victim = await commands.MemberConverter().convert(ctx, x)
            try:
                await victim.move_to(self.bot.get_channel(ctx.author.voice.channel.id))
            except Exception as e:
                logging.error(f"moving of {victim.name} failed: {e}")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")


    @coordinator.command(help="Flips a coin")
    @commands.has_any_role(*coord_roles_ids)
    async def coin(self, ctx):
        logging.info("Coin ran")
        if getrandbits(1) == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")
        logging.info("Coin ended\n-------------")


    @coordinator.command(help="Picks a random user in your vc")
    @commands.has_any_role(*coord_roles_ids)
    async def pick_user(self, ctx):
        logging.info("pick_use invoked")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Picking user in {voice.name}")
        valid_users = []
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        valid_users.append(member.name)
                        logging.info(f"{x.name} valid")
            else:
                valid_users.append(member.name)
                logging.info(f"{x.name} valid")
        await ctx.send(choice(valid_users))
        logging.info("pick_user concluded\n-------------")

    @coordinator.command(aliases=["pick_num","p_n"], help="Picks a random number inbetween 1 and the given argument")
    @commands.has_any_role(*coord_roles_ids)
    async def pick_number (self, ctx, value: int):
        logging.info(f"pick_number invoked in {ctx.guild.name}")
        await ctx.send(randint(1,value))
        logging.info("pick_number concluded\n-------------")


def setup(bot):
    bot.add_cog(Coord(bot))
