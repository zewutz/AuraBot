import discord
from discord.ext import commands


class Model(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #Create group
    @commands.group(invoke_without_command=True)
    async def create_group_(self, ctx):
        pass

    #Create command
    @create_group_.command(name="command_name", pass_context=True)
    async def create_command(self, ctx):
        pass

    @commands.command()
    async def test(self, ctx):
        await ctx.send("hello")
    
def setup(client):
    client.add_cog(Model(client))