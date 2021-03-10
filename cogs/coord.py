import logging
from discord.ext import commands


lobby_vc_id = int(764546987441258506) # tourney time vc
coord_roles_ids = [785420213801582593, 785420338673614848, 785420354440921109, 775663293695524905] # owner perms, admin perms, mod perms, coordinator
ignored_roles = ["810492978816090173"] #spectator


class coord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(case_insensitive=True, aliases=["m"], help="Mutes users in your vc. alias = m")
    @commands.has_any_role(*coord_roles_ids)
    async def mute(self, ctx):
        logging.info("coord mute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"muting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            for xd in ignored_roles:
                logging.info(f"checking for ignored role: {xd}")
                if xd in str(member.roles):
                    logging.info(f"{x.name} ignored")
                    continue
                else:
                    await member.edit(mute=True, deafen=True)
                    logging.info(f"{x.name} muted")
        await ctx.message.delete()
        logging.info("Finished muting\n-------------")

    @commands.command(case_insensitive=True, aliases=["um"])
    @commands.has_any_role(*coord_roles_ids)
    async def unmute(self, ctx):
        logging.info("coord unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"unmuting in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.mute is True:
                await member.edit(mute=False, deafen=False)
                logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting\n-------------")
    
    @commands.command(case_insensitive=True, aliases=["mout"])
    @commands.has_any_role(*coord_roles_ids)
    async def move_out(self, ctx):
        logging.info("coord move_in ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            for xd in ignored_roles:
                logging.info(f"checking for ignored role: {xd}")
                if xd in str(member.roles):
                    logging.info(f"{x.name} ignored")
                    continue
                else:
                    await member.move_to(self.bot.get_channel(lobby_vc_id))
                    logging.info(f"{x.name} moved")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")

    @commands.command(case_insensitive=True, aliases=["min"])
    @commands.has_any_role(*coord_roles_ids)
    async def move_in(self, ctx, *, argument):
        logging.info("coord move_in ran")
        victims = argument.split() # I thought "victims" was a funny variable name for the users being moved :)
        logging.info(victims)
        for x in victims:
            if x.isdigit():
                victim = ctx.guild.get_member(int(x))
            else:
                ID = x[3:]
                ID = ID[:-1]
            victim = ctx.guild.get_member(int(ID))
            if victim is None:
                logging.info("victim is None, continuing")
                continue
            logging.info(victim)
            try:
                await victim.move_to(self.bot.get_channel(ctx.author.voice.channel.id))
            except Exception as e:
                logging.error(f"moving of {victim.name} failed: {e}")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")

def setup(bot):
    bot.add_cog(coord(bot))