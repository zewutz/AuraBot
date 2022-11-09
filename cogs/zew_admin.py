import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # Clear command
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        try:
            await ctx.channel.purge(limit=amount)
        except Exception as ext:
            print(ext)

    @clear.error
    async def clear_errors(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.orange())
            embed.add_field(name="Warning!", value="You do not have the appropriate permission(s) to run this command.", inline=False)
            embed.set_footer(text="Manage Messages permission(s) required!")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.red())
            embed.add_field(name="Warning!", value="I don't have sufficient permission(s)!", inline=False)
            embed.set_footer(text="Manage Messages permission(s) required!")
            await ctx.send(embed=embed)



    # Kick command
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, * , reason = None):
        KickedOutFormats = ["has been kicked out.",
                                      "has been thrown out.",
                                      "has been expelled from this guild.",
                                      "has been removed from this guild.",
                                      "has been projected into another guild."]
        try:
            await member.kick(reason=reason)
            embed=discord.Embed(title="new kick case", color=discord.Color.orange(), timestamp=datetime.datetime.now())
            embed.add_field(name=f"{member} {random.choice(KickedOutFormats)}", value=f"Moderator: {ctx.author.name}\nReason: {reason}", inline=False)
            embed.set_footer(text=f'ID: {str(member.id)}')

            await ctx.send(embed=embed)

        except Exception as ext:
            print(ext)

    @kick.error
    async def kick_errors(self, ctx, error):
        prefix = ''.join(get_prefix(self.client, ctx))
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title=" ", color=discord.Color.green())
            embed.add_field(name="Kick Command Format", value=f"`{prefix}kick (member) [reason]`", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.orange())
            embed.add_field(name="Warning", value="You do not have the appropriate permission(s) to run this command.", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.red())
            embed.add_field(name="Warning", value="I don't have sufficient permission(s)!", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)



    # Ban command
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, * , reason = None):
        BannedFormats = ["has been blacklisted from this guild.",
                         "has been banned from this guild.",
                         "has been excluded from this guild.",
                         "has been restricted from this guild."]
        try:
            await member.ban(reason=reason)
            embed=discord.Embed(title="new ban case", color=discord.Color.orange(), timestamp=datetime.datetime.now())
            embed.add_field(name=f"{member} {random.choice(BannedFormats)}", value=f"Moderator: {ctx.author.name}\nReason: {reason}", inline=False)
            embed.set_footer(text=f'ID: {str(member.id)}')

            await ctx.send(embed=embed)
        except Exception as ext:
            print(ext)

    @ban.error
    async def ban_errors(self, ctx, error):
        prefix = ''.join(get_prefix(self.client, ctx))
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title=" ", color=discord.Color.green())
            embed.add_field(name="Ban Command Format", value=f"`{prefix}ban (member) [reason]`", inline=False)
            embed.set_footer(text="In order to use this command you require `ban members` permission")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.orange())
            embed.add_field(name="Warning", value="You do not have the appropriate permissions to run this command.", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.red())
            embed.add_field(name="Warning", value="I don't have sufficient permissions!", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)


    # Unban command
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason=None):
        UnbanFormats = ["has been unbanned.","has been forgiven."]
        try:
            await ctx.guild.unban(member)  #!Unban user Send embed
            embed=discord.Embed(title="User unbanned", color=discord.Color.dark_green(), timestamp=datetime.datetime.now())
            embed.add_field(name=f"{member} {random.choice(UnbanFormats)}", value=f"Moderator: {ctx.author.name}\nReason: {reason}", inline=False)
            embed.set_footer(text=f'ID: {str(member.id)}')
            await ctx.send(embed=embed)

        except Exception as ext:
            print(ext)

    @unban.error
    async def unban_errors(self, ctx, error):
        prefix = ''.join(get_prefix(self.client, ctx))
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title=" ", color=discord.Color.green())
            embed.add_field(name="Unban Command Format", value=f"`{prefix}unban (member) [reason]`", inline=False)
            embed.set_footer(text="In order to use this command you require `ban members` permission(s)")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.orange())
            embed.add_field(name="Warning!", value="You do not have the appropriate permission(s) to run this command.", inline=False)
            embed.set_footer(text="Kick members permission(s) required!")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.red())
            embed.add_field(name="Warning!", value="I don't have sufficient permission(s)!", inline=False)
            embed.set_footer(text="Ban members permission(s) required!")
            await ctx.send(embed=embed)


    # Change prefix
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True) 
    async def changeprefix(self, ctx, prefix):
        try: 
            DB.change_prefix(ctx.guild.id, prefix)
            await ctx.send(f'Prefix changed to: {prefix}')

        except Exception as ext:
            print(ext)

    @changeprefix.error
    async def changeprefix_errors(self, ctx, error):
        prefix = ''.join(get_prefix(self.client, ctx))
        if isinstance(error, MissingRequiredArgument):
            embed=discord.Embed(title=" ", color=discord.Color.green())
            embed.add_field(name="Missing Required Argument", value=f"`{prefix}changeprefix (prefix)`", inline=False)
            embed.set_footer(text="Administrator permission(s) required!")
            await ctx.send(embed=embed)

        if isinstance(error, MissingPermissions):
            embed=discord.Embed(title=" ", color=discord.Color.orange())
            embed.add_field(name="Warning!", value="You do not have the appropriate permission(s) to run this command.", inline=False)
            embed.set_footer(text="Administrator permission(s) required!")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Admin(client))
