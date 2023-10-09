import io
import discord
from settings import TOKEN
import aiohttp

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"logged as {bot.user}")

@bot.slash_command(name='ping',description='replies to the bot ping')
async def ping(ctx):
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')

#echo command
@bot.slash_command(name='echo',description='replies with the same message')
async def echo(ctx,*,message):
    await ctx.respond(message)



# meme command
@bot.slash_command(name='meme',description='search the web for a meme image')
async def meme(ctx,text1:str,text2:str):
    if text1 == None or text2 == None:
        return await ctx.respond('please provide 2 texts')
    
    meme_name = f'{text1}/{text2}'
    d = {' ': '_', '/': '~s', '?': '~q', '%': '~p', '#': '~h', '+': '~p', '"': "''"}
    for k, v in d.items():
        meme_name = meme_name.replace(k, v)

    meme_url = f'https://memegen.link/touch/{meme_name}/.jpg'
    await ctx.respond(meme_url)

    
    
    


bot.run(TOKEN)
