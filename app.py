import discord
from gradio_client import Client
import os
import threading
import gradio as gr
from threading import Event

event = Event()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

client = Client("tiiuae/falcon-180b-demo")
def predict(text):
    return client.predict(text,"", 0.9, 256, 0.95, 1.0)

@bot.event
async def on_ready():
    print(f"logged as {bot.user}")
    event.set()

@bot.slash_command(name='ping',description='replies to the bot ping')
async def ping(ctx):
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')

#echo command
@bot.slash_command(name='echo',description='replies with the same message')
async def echo(ctx,*,message):
    await ctx.respond(message)



# AI prediction command
@bot.slash_command(name='ask',description='ask falcon-180b-demo AI')
async def ask(ctx,*,question):
    await ctx.respond(question)
    try : 
        prediction = predict(question)
        await ctx.respond(prediction)
    except Exception as e: 
        await ctx.respond(e)


# running in thread
def run_bot():
    if not DISCORD_TOKEN:
        print("DISCORD_TOKEN NOT SET")
        event.set()
    else:
        bot.run(DISCORD_TOKEN)


threading.Thread(target=run_bot).start()
event.wait()

with gr.Blocks() as demo:
    gr.Markdown("## Falcon-180b-demo")


demo.launch()