import os
import requests
import urllib.parse
from discord import Intents
from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

load_dotenv()
token = os.environ['token']
telegram_token = os.environ['telegram_token']
chatid = os.environ['chatid']
webhookurl = os.environ['webhookurl']
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
caption = ""
normal_words = ['i', 'the', 'hi', 'and', 'to', 'a', 'it', 'is', 'in', 'you']

iddict = {
    "telegramid": "discordid"
}

def downloader(fileid):
    global filepath
    r = requests.get(
        f'https://api.telegram.org/bot{telegram_token}/getFile?file_id={fileid}'
    )
    filepath = r.json()['result']['file_path']

    r = requests.get(
        f'https://api.telegram.org/file/bot{telegram_token}/{filepath}')

    with open(filepath.split("/")[-1], 'wb') as file:
        file.write(r.content)

    if caption != "":
        webhook = DiscordWebhook(
            url=webhookurl,
            username=user,
            avatar_url=f"https://cdn.discordapp.com/avatars/{iddict[id]}/{pfp}",
            content=caption)
        with open(file=filepath.split("/")[-1], mode='rb') as f:
            webhook.add_file(file=f.read(), filename=filepath.split("/")[-1])
        webhook.execute()
        os.remove(filepath.split("/")[-1])
    else:
        webhook = DiscordWebhook(
            url=webhookurl,
            username=user,
            avatar_url=f"https://cdn.discordapp.com/avatars/{iddict[id]}/{pfp}"
        )
        with open(file=filepath.split("/")[-1], mode='rb') as f:
            webhook.add_file(file=f.read(), filename=filepath.split("/")[-1])
        webhook.execute()
        os.remove(filepath.split("/")[-1])

def getdiscinfo(id):
    global pfp
    global user
    a = requests.get(f"https://discord.com/api/v10/users/{iddict[id]}",
                     headers={"Authorization": f"Bot {token}"})
    pfp = a.json()["avatar"]
    user = a.json()["username"]

@tasks.loop(seconds=0.15)
async def telegram_check():
    global result
    global previous
    global previousfileid
    global r
    global id
    r = requests.post(
        f"https://api.telegram.org/bot{telegram_token}/getUpdates?offset=-1")

    id = r.json()['result'][0]['message']['from']['id']

    try:
        fileid = r.json()['result'][0]['message']['document']['file_id']
        if fileid != previousfileid:
            try:
                caption = r.json()['result'][0]['message']['caption']
            except:
                pass
            getdiscinfo(id)
            downloader(fileid, caption)
            previousfileid = fileid
    except:
        try:
            fileid = r.json()['result'][0]['message']['photo'][-1]['file_id']
            if fileid != previousfileid:
                try:
                    caption = r.json()['result'][0]['message']['caption']
                except:
                    pass
                getdiscinfo(id)
                downloader(fileid)
                previousfileid = fileid
        except:
            try:
                fileid = r.json()['result'][0]['message']['video']['file_id']
                if fileid != previousfileid:
                    try:
                        caption = r.json()['result'][0]['message']['caption']
                    except:
                        pass
                    getdiscinfo(id)
                    downloader(fileid)
                    previousfileid = fileid
            except:
                try:
                    result = r.json()['result'][0]['message']['text'].split()
                    for i in range(len(result)):
                        if result[i] == "@everyone":
                            result[i] = "."
                        elif result[i] == "@here":
                            result[i] = "."
                        else:
                            pass
                    result = " ".join(result)
                    id = r.json()['result'][0]['message']['from']['id']
                    if result != previous:
                        getdiscinfo(id)
                        webhook = DiscordWebhook(
                            url=webhookurl,
                            username=user,
                            avatar_url=
                            f"https://cdn.discordapp.com/avatars/{iddict[id]}/{pfp}",
                            rate_limit_retry=True,
                            content=result)
                        webhook.execute()
                    elif result == previous:
                        pass
                    previous = result
                except:
                    pass

@bot.event
async def on_message(message):
    global replymsg
    msg = message
    msgcontent = msg.content
    if msg.reference != None:
        channel = bot.get_channel(msg.reference.channel_id)
        messagething = await channel.fetch_message(msg.reference.message_id)
        replymsg = messagething.content
    else:
        replymsg = ""

    await bot.process_commands(message)

    if message.author.bot == False:
        global msg1
        global msg2
        files = ""
        try:
            for i in message.attachments:
                files = files + f'{i}\n'
            msg1 = urllib.parse.quote(
                f"{message.author.name}#{message.author.discriminator} - {msgcontent}\n{files}"
            )
        except:
            msg1 = urllib.parse.quote(
                f"{message.author.name}#{message.author.discriminator} - {msgcontent}"
            )
        if replymsg != "":
            msg2 = urllib.parse.quote(f"Replying to: {replymsg}")
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg2}\n{msg1}"
            )
        else:
            requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg1}"
            )

@bot.event
async def on_ready():
    print(
        f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')
    telegram_check.start()

global previous
global previousfileid
r = requests.post(
    f"https://api.telegram.org/bot{telegram_token}/getUpdates?offset=-1")
try:
    result = r.json()['result'][0]['message']['text'].split()
    for i in range(len(result)):
        if result[i] == "@everyone":
            result[i] = "."
        elif result[i] == "@here":
            result[i] = "."
        else:
            pass
    previous = " ".join(result)
except:
    previous = ""

previousfileid = ""

try:
    bot.run(token)
except:
    os.system('kill 1')
