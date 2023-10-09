import discord
from settings import TOKEN
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"logged as {bot.user}")

@bot.slash_command(name='ping',description='replies to the bot ping')
async def ping(ctx):
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')


bot.run(TOKEN)
