import discord
from gradio_client import Client
import os
import threading
import gradio as gr
from threading import Event

event = Event()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

client = Client("tiiuae/falcon-180b-demo")
def predict(text,history=""):
    return client.predict(text,history, 0.9, 256, 0.95, 1.0)

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
@bot.slash_command(name='falcon180b',description='ask falcon-180b-demo AI')
async def falcon180b(ctx,*,question):
    # channel = bot.get_channel(ctx.channel_id)
    # if channel name is falcon-180b-demo
    if ctx.channel.name == "falcon-180b-demo":
        await ctx.respond(f"Creating a thread for {ctx.author.mention} ")
        try : 
            # preparing the prediction before creating the thread
            prediction = predict(question)
            thread =  await ctx.channel.create_thread(name=question,type=discord.ChannelType.public_thread) 
            await thread.send(prediction)
        except Exception as e: 
            await thread.send(e)
    else:
        await ctx.respond(f"Please use this command in the channel falcon-180b-demo")

@bot.event
async def on_message(message):
    """
    continue the chat in the thread
    """
    # if the message is from the bot ignore it
    if message.author == bot.user:
        return
    # if the message is from the thread
    if message.channel.type == discord.ChannelType.public_thread:
        # if the message is from the bot ignore it
        if message.author == bot.user:
            return
        # FIX THIS !!!!!!!!!!!!
        print("the content of the message is ", message.content) # WORKS WITH INTENTS
        print("the author of the message is ", message.author) # me :p 
        print("the channel of the message is ", message.channel) # hello
        print("the type of the channel of the message is ", message.channel.type) # public_thread
        print("the parent of the thread of the message is ", message.channel.parent) # falcon-180b-demo
        print("the id of the thread of the message is ", message.channel.id) # channel_id: int 
    #     # preparing the prediction
    #     prediction = predict(message.content,"")
    #     # send the prediction
    #     await message.reply(prediction)
    # await bot.process_commands(message)
    


# setup create the falcon-180b-demo channel
@bot.slash_command(name='setup',description='setup the bot')
async def setup(ctx):
    # if channel falcon-180b-demo doesn't exist create it
    if not discord.utils.get(ctx.guild.channels, name="falcon-180b-demo"):
        await ctx.guild.create_text_channel("falcon-180b-demo",category=ctx.channel.category)
        ctx.respond("falcon-180b-demo channel created")
    else:
        await ctx.respond("falcon-180b-demo channel already exist")


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