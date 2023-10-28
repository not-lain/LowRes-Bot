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





# AI prediction command
@bot.slash_command(name='falcon180b',description='ask falcon-180b-demo AI')
async def falcon180b(ctx,*,question):
    """ 
    AI command to create the thread and ask the AI
    """
    # if channel name is falcon-180b-demo
    try:
        if ctx.channel.name == "falcon-180b-demo":
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
            # tag the channel #falcon-180b-demo
            # create the channel if we can't find it, tag it and let the user know that we created it
            await ctx.respond(f"""
                              use this command in the channel #falcon-180b-demo\nuse `/setup` to create the channel if it doesn't exist""")
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
            # if the thread is falcon-180b-demo
            if message.channel.parent.name == "falcon-180b-demo":
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
    
            



# setup create the falcon-180b-demo channel
@bot.slash_command(name='setup',description='setup the bot')
async def setup(ctx):
    """
    create the #falcon-180b-demo channel
    """
    # if channel falcon-180b-demo doesn't exist create it
    if not discord.utils.get(ctx.guild.channels, name="falcon-180b-demo"):
        await ctx.guild.create_text_channel("falcon-180b-demo",category=ctx.channel.category)
        await ctx.respond("falcon-180b-demo channel created")
    else:
        # TODO: tag the channel
        await ctx.respond("#falcon-180b-demo channel already exist")


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