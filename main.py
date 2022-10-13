# Imports
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import json
#from keep_alive import keep_alive
from discord.utils import get
####
token = "MTAyOTYwNzY1NTI3MjEwMzkzNg.GLBVA1.m-hVT94YVEHFbHtqqdbhsyYLKBZ-Wxsl7pexJQ"
###
intents = discord.Intents.all()
####

# Prefix


client = commands.Bot(command_prefix='?', intents=intents)

####
status = cycle(["Use ?help","Join my Server"])
####


# Tasks
@tasks.loop(seconds=5)
async def status_change():
	await client.change_presence(status=discord.Status.online,activity=discord.Game(next(status)))
# On Ready Message
@client.event
async def on_ready():
	print("SudoBot is Ready to Code\nHave Fun")
	status_change.start()

#Give role command	
@client.command(pass_context=True)
async def give_role(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"Hey {user.name}! {ctx.author.name} role was given to you by {ctx.author.name} ")
# remove role command
@client.command(pass_context=True)
async def remove_role(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"Hey {user.name}, {ctx.author.name} has been removed a role called: {role.name}")


	


# On Member Join
@client.event
async def on_member_join(member):
	print(f"{member} Has Joined")
	
# On Member Leave
@client.event
async def on_member_remove(member):
	print(f"{member} Has Left the Server")
# Error Event
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.author.send("Please Pass In All Required Arguments")
# Bot Ping Command
@client.command()
async def ping(ctx):
	await ctx.author.send(f"**Pong!** The Ping is {round(client.latency * 1000)}ms")
	print("Sent Message")
# Clear Command
@client.command(aliases=["purge","remove"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)
	await ctx.author.send(f'Cleared {amount} Messages.')
	print("Sent Message")

# fun rate Command
@client.command()
async def rate(ctx):
    await ctx.send(f'You are {randrange(101)}% Cool')
#    await ctx.send("You are Cool")


# Kick Command
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *,reason=None):
	await member.kick(reason = reason)
	await ctx.author.send(f"Kicked {member} From the Server.")
# Ban Command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *,reason=None):
	await member.ban(reason = reason)
	await ctx.author.send(f"Banned {member} From the Server.")
# Unban Command
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split("#")

	for ban_entry in banned_users:
		user = ban_entry.user 

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.author.send(f"Unbanned {user}#{user.discriminator} From the Server")
			await user.send('You have been Unbanned')



	
# Dont touch
# # Cog load
# @client.command()
# async def load(ctx, extension):
# 	client.load_extension(f'cogs.{extension}')
# # Cog unload
# @client.command()
# async def unload(ctx, extenstionion):
# 	client.unload_extension(f'cogs.{extension}')
# for filename in os.listdir("./cogs"):
# 	if filename.endswith(".py"):
# 		client.load_extension(f"cogs.{filename[:-3]}")
#keep_alive()

client.run(token)
