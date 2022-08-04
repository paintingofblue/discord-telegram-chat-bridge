import os
import requests
import urllib.parse
from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

load_dotenv()
token = os.getenv('token')
telegram_token = os.getenv('telegram_token')
chatid = os.getenv('chatid')
webhookurl = os.getenv('webhook')
bot = commands.Bot(command_prefix="!")
previous = ''

discid = {
    putteleanddiscidshere: "only optional if you want automatic pfp and username on webook"
}

@tasks.loop(seconds=0.25)
async def telegram_check():
    global result
    global previous
    global r
    r = requests.post(
        f"https://api.telegram.org/bot{telegram_token}/getUpdates?offset=-1")
    try:
        result = r.json()['result'][0]['message']['text']
        id = r.json()['result'][0]['message']['from']['id']
        discid = iddict[id]
        if result != previous:
            a = requests.get(f"https://discord.com/api/v10/users/{iddict[id]}",
                             headers={"Authorization": f"Bot {token}"})
            pfp = a.json()["avatar"]
            user = a.json()["username"]
            webhook = DiscordWebhook(
                url=webhookurl, username=user, avatar_url=f"https://cdn.discordapp.com/avatars/{discid}/{pfp}", rate_limit_retry=True, content=result) 
            webhook.execute()
        elif result == previous:
            pass
        previous = result
    except:
        pass


@bot.event
async def on_message(message):
    if message.author.bot == False:
        global msg
        global msg1
        global msg2
        msg1 = urllib.parse.quote(f"{message.author.name}#"
                                  f"{message.author.discriminator} - " +
                                  f"{message.content}")
        try:
            if message.reference.cached_message != "None":
                msg2 = urllib.parse.quote(
                    f"Replying to: {message.reference.cached_message.content}")
                requests.post(
                    f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg2}\n{msg1}"
                )
        except:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg1}"
            )
        else:
            pass


@bot.event
async def on_ready():
    print(
        f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')
    telegram_check.start()


bot.run(token)
