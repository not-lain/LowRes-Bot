import discord
from settings import TOKEN
from gradio_client import Client
from fastapi import FastAPI
import asyncio

bot = discord.Bot()

client = Client("tiiuae/falcon-180b-demo")
def predict(text):
    return client.predict(text,"", 0.9, 256, 0.95, 1.0)

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
    
    d = {' ': '_', '/': '~s', '?': '~q', '%': '~p', '#': '~h', '+': '~p', '"': "''"}
    for k, v in d.items():
        text1 = text1.replace(k, v)
        text2 = text2.replace(k, v)
    meme_name = f'{text1}/{text2}'

    meme_url = f'https://memegen.link/touch/{meme_name}/.jpg'
    await ctx.respond(meme_url)


# AI prediction command
@bot.slash_command(name='ask',description='ask falcon-180b-demo AI')
async def ask(ctx,*,question):
    await ctx.respond(question)
    try : 
        prediction = predict(question)
        await ctx.respond(prediction)
    except Exception as e: 
        await ctx.respond(e)
    
# bot.run(TOKEN)


app = FastAPI()
@app.on_event("startup")
async def startup():
    try : 
        if not TOKEN:
            print("DISCORD_TOKEN NOT SET")
        else:
            asyncio.create_task(bot.start(TOKEN))
            print("Bot started")
    except Exception as e:
        print(e)



