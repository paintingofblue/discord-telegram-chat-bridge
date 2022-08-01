import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('TOKEN')
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_message():
    print("")

@bot.event
async def on_ready():
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')


bot.run(TOKEN)