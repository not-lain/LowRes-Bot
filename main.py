import discord
from discord.ext import commands
with open('token.txt', 'r') as f:
    token = f.read()


# client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(command_prefix = '!',intents=discord.Intents.default()) # Create a new bot instance


@client.event # Event decorator/wrapper
async def on_ready():
    print('Bot is ready')
    print("------------------")

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')




client.run(token) # Run the bot


