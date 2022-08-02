import os
import requests
import urllib.parse
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')
telegram_token = os.getenv('telegram_token')
chatid = os.getenv('chatid')
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_message(message):
    global msg
    global msg1
    global msg2
    msg1 =  urllib.parse.quote(f"{message.author.name}#"f"{message.author.discriminator} - " + f"{message.content}")
    try:
        if message.reference.cached_message != "None":
            msg2 = urllib.parse.quote(f"Replying to: {message.reference.cached_message.content}")
            requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg2}\n{msg1}")
    except:
        requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg1}")

@bot.event
async def on_ready():
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')

bot.run(token)