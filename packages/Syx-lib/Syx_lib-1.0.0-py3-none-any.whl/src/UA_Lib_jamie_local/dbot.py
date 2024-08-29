import discord
from discord.ext import commands
import logging
import random
import datetime


# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the bot's command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    logging.info(f'Bot is online! Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')


@bot.command(name='ping', help='Check the bot\'s latency.')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", color=discord.Color.blue())
    embed.add_field(name="Latency", value=f"{latency}ms")
    await ctx.send(embed=embed)

# Echo Command
@bot.command(name='echo', help='Echo the provided message.')
async def echo(ctx, *, message: str):
    embed = discord.Embed(title="🔊 Echo", description=message, color=discord.Color.green())
    await ctx.send(embed=embed)

# Server Info Command
@bot.command(name='info', help='Provide information about the server.')
async def info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"ℹ️ Server Information", color=discord.Color.purple())
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

# Coin Flip Command
@bot.command(name='coinflip', help='Flip a coin.')
async def coinflip(ctx):
    result = random.choice(['Heads', 'Tails'])
    embed = discord.Embed(title="🪙 Coin Flip", description=f"The result is **{result}**!", color=discord.Color.gold())
    await ctx.send(embed=embed)

# Dice Roll Command
@bot.command(name='roll', help='Roll a die.')
async def roll(ctx, sides: int = 6):
    result = random.randint(1, sides)
    embed = discord.Embed(title="🎲 Dice Roll", description=f"You rolled a **{result}** on a {sides}-sided die!", color=discord.Color.red())
    await ctx.send(embed=embed)

# Avatar Command
@bot.command(name='avatar', help='Get your or another user\'s avatar.')
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# Clear Messages Command
@bot.command(name='clear', help='Clear a number of messages.')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title="🧹 Messages Cleared", description=f"{amount} messages have been cleared.", color=discord.Color.orange())
    await ctx.send(embed=embed, delete_after=5)

# Ban Command
@bot.command(name='ban', help='Ban a user from the server.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 User Banned", description=f"{member.mention} has been banned.", color=discord.Color.dark_red())
    embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
    await ctx.send(embed=embed)

# Kick Command
@bot.command(name='kick', help='Kick a user from the server.')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title="👢 User Kicked", description=f"{member.mention} has been kicked.", color=discord.Color.dark_orange())
    embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
    await ctx.send(embed=embed)



# Random Joke Command
@bot.command(name='joke', help='Get a random joke.')
async def joke(ctx):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "What do you call cheese that isn't yours? Nacho cheese.",
        "Why couldn't the bicycle stand up by itself? It was two-tired.",
        "I'm reading a book about anti-gravity. It's impossible to put down.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    embed = discord.Embed(title="😂 Here's a joke for you!", description=random.choice(jokes), color=discord.Color.magenta())
    await ctx.send(embed=embed)

# Random Number Generator Command
@bot.command(name='random', help='Generate a random number between 1 and a given number.')
async def random_number(ctx, max_num: int):
    number = random.randint(1, max_num)
    embed = discord.Embed(title="🔢 Random Number Generator", description=f"Your random number is **{number}**", color=discord.Color.teal())
    await ctx.send(embed=embed)

# Server Roles Command
@bot.command(name='roles', help='List all roles in the server.')
async def roles(ctx):
    roles = ', '.join([role.name for role in ctx.guild.roles if role.name != "@everyone"])
    embed = discord.Embed(title="📝 Server Roles", description=roles, color=discord.Color.dark_blue())
    await ctx.send(embed=embed)

# DM Command
@bot.command(name='dm', help='Send a DM to a user.')
async def dm(ctx, member: discord.Member, *, content: str):
    try:
        await member.send(content)
        embed = discord.Embed(title="📤 DM Sent", description=f"Your message to {member.mention} was sent successfully.", color=discord.Color.green())
    except discord.Forbidden:
        embed = discord.Embed(title="❌ Failed to Send DM", description=f"Could not send a DM to {member.mention}.", color=discord.Color.red())
    await ctx.send(embed=embed)

# Hug Command
@bot.command(name='hug', help='Send a virtual hug to someone.')
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(title="🤗 Hug", description=f"{ctx.author.mention} sends a warm hug to {member.mention}!", color=discord.Color.pink())
    await ctx.send(embed=embed)


# Current Time Command
@bot.command(name='time', help='Get the current UTC time.')
async def time(ctx):
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    embed = discord.Embed(title="🕒 Current Time", description=current_time, color=discord.Color.dark_green())
    await ctx.send(embed=embed)
@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="❌ Error", color=discord.Color.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Details", value="Missing required argument.", inline=False)
    elif isinstance(error, commands.CommandNotFound):
        embed.add_field(name="Details", value="Command not found.", inline=False)
    else:
        embed.add_field(name="Details", value="An error occurred while processing the command.", inline=False)

    await ctx.send(embed=embed)
    logging.error(f'Error in command {ctx.command}: {error}')


def token(token):
    bot.run(token)
