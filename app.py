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

client = Client("hysts/mistral-7b")
def predict(text,history=""):
    return client.predict(text,history, 0.9, 256, 0.95, 1.0)

@bot.event
async def on_ready():
    print(f"logged as {bot.user}")
    event.set()



# AI prediction command
@bot.slash_command(name='mistral7b',description='ask mistral-7b-demo AI')
async def mistral7b(ctx,*,question):
    """ 
    AI command to create the thread and ask the AI
    """
    # if channel name is mistral7b
    try:
        if ctx.channel.name == "mistral7b":
            await ctx.respond(f"Creating a thread for {ctx.author.mention} ...")
            try : 
                # preparing the prediction before creating the thread
                # need to make sure AI sends the first message
                prediction = predict(question)
                thread =  await ctx.channel.create_thread(name=question,type=discord.ChannelType.public_thread) 
                await thread.send(prediction)
            except Exception as e: 
                await thread.send(e)
        else:
            # TODO:
            # tag the channel #mistral7b
            # create the channel if we can't find it, tag it and let the user know that we created it
            await ctx.respond(f"""
                              use this command in the channel #mistral7b\nuse `/setup` to create the channel if it doesn't exist""")
    except Exception as e:
        await ctx.respond(e)

@bot.event
async def on_message(message):
    """
    continue the chat in the thread
    """
    # if the message is from the bot ignore it
    if message.author != bot.user:
        # if the message is from the thread
        if message.channel.type in [ discord.ChannelType.public_thread, discord.ChannelType.private_thread ]:
            # if the thread is mistral7b
            if message.channel.parent.name == "mistral7b":
                # preparing the prediction
                # get channel's last 10 messages
                history = await message.channel.history(limit=10).flatten()
                # remove the first message which is the question
                prompt = history.pop(0)
                print("prompt :",prompt.content)
                print("history is ")
                for h in history:
                    print(f"{h.author} : {h.content}")
                # TODO: prepare the history for the prediction                 
                # predict the response
                prediction = predict(message.content,history="") 
                await message.channel.send(prediction)
    
            



# setup create the mistral7b channel
@bot.slash_command(name='setup',description='setup the bot')
async def setup(ctx):
    """
    create the #mistral7b channel
    """
    # if channel mistral7b doesn't exist create it
    if not discord.utils.get(ctx.guild.channels, name="mistral7b"):
        await ctx.guild.create_text_channel("mistral7b",category=ctx.channel.category)
        await ctx.respond("mistral7b-demo channel created")
    else:
        # TODO: tag the channel
        await ctx.respond("#mistral7b channel already exist")


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
    gr.Markdown("## mistral7b")


demo.launch()
