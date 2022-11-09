import discord
from discord.ext import commands
import os

class BotStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        return

    @commands.group(name="bot", invoke_without_command=True)
    async def bot(self, ctx):
        await ctx.send("*In construction.*\n\n**Contact**\n*Discord*: zewutz#1974\n*Email*: zewutz@gmail.com\n*Instagram*: @zewutz")

    @bot.command(name="ping")
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f"[PING] {round(self.client.latency * 1000)}ms")

    @bot.command(name="leave")
    @commands.is_owner()
    async def leave_guild(self, ctx, confirm):
        if confirm.lower() == "confirm":
            await ctx.guild.leave()

    @bot.command(name="guilds")
    @commands.is_owner()
    async def botguilds(self, ctx):
        guild_number = f"{self.client.user.mention} currently connected to {len(list(self.client.guilds))} servers."
        await ctx.send(guild_number)


from database import DB
class DBManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        return

    @commands.is_owner()
    @commands.group(name="db", invoke_without_command=True)
    async def database_(self, ctx):
        await ctx.send("Database Interface running..")


    @commands.is_owner()
    @database_.command(name="table")
    async def viewTable(self, ctx, tablename):
        return

    @commands.is_owner()
    @database_.command(name="adduser")
    async def addUser(self, ctx ,member : discord.Member):
        print(member)
        member_name = member.name
        member_tag = str(member)[-4:]
        member_id = member.id

        if member.bot is False:
            DB.add_user(member_name, member_tag, member_id)
            await ctx.send(f"{member} inserted into database.")
        elif member.bot is True:
            await ctx.send(f"{member} is a bot. ")

    @commands.is_owner()
    @database_.command(name="addguildmembers")
    async def addAllGuildMembers(self, ctx):
        members = ctx.guild.members
        for member in members:
            if member.bot is False:
                result = DB.fetch_user(member.id)
                if result is False:
                    DB.add_user(member.name, str(member)[-4:], member.id)
            else:
                continue

        print("All guild members are now in the DB.")



    @commands.is_owner()
    @database_.command(name="addguild")
    async def addGuild(self, ctx ,guild : discord.Guild):
        print(guild)
        guild_id = guild.id
        guild_prefix = '*'


        DB.add_guild(guild_id, guild_prefix)
        await ctx.send(f"{guild} inserted into database.")



def setup(client):
    client.add_cog(BotStatus(client))
    client.add_cog(DBManagement(client))