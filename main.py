import os
import requests
import urllib.parse
import json
from discord import Embed, Intents
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
s = requests.Session()

iddict = {
    5099235928: "351931183770238976",
    5223393878: "986082432551882843",
    1800315640: "884947813744640020",
    5787521593: "884947813744640020",
    5519126994: "700548055220617297",
    1993888374: "477292494468546580",
    5653290999: "663993010459115521",
    5528500209: "795579890761596972",
}


def downloader(fileid, caption):
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
    a = requests.get(f"https://discord.com/api/v10/users/{iddict[id]}", headers={"Authorization": f"Bot {token}"})
    pfp = a.json()["avatar"]
    user = a.json()["username"]


@tasks.loop(seconds=0.15)
async def telegram_check():
    try:
        global result
        global previous
        global previousfileid
        global r
        global id
        r = s.get(f'https://api.telegram.org/bot{telegram_token}/getUpdates?offset=-1')

        id = r.json()['result'][0]['message']['from']['id']

        try:
            fileid = r.json()['result'][0]['message']['document']['file_id']
            if fileid != previousfileid:
                try:
                    caption = r.json()['result'][0]['message']['caption']
                except:
                    caption = ''
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
                        caption = ''
                    getdiscinfo(id)
                    downloader(fileid, caption)
                    previousfileid = fileid
            except:
                try:
                    fileid = r.json()['result'][0]['message']['video']['file_id']
                    if fileid != previousfileid:
                        try:
                            caption = r.json()['result'][0]['message']['caption']
                        except:
                            caption = ''
                        getdiscinfo(id)
                        downloader(fileid, caption)
                        previousfileid = fileid
                except:
                    try:
                        result = r.json(
                        )['result'][0]['message']['text'].split()
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
                            previous = result
                    except:
                        pass
    except:
        pass


@bot.command()
async def lb(ctx, type, *args):
    try:
        arg = args[0]
    except:
        arg = ""
    guildid = str(ctx.guild.id)
    guildname = str(ctx.guild.name)
    if type == "person":
        if "<@" in arg:
            arg = str(arg.split("<@")[1].split(">")[0])
            try:
                with open('data.json', 'r', encoding='utf8') as file:
                    data = json.load(file)
                    sortedDict = dict(
                        sorted(data[guildid][arg].items(),
                               key=lambda kv: kv[1],
                               reverse=True))
                    count = 0
                    tag = await bot.fetch_user(arg)
                    embed = Embed(
                        title=f"{tag}'s 10 most used words in this server")
                    while True:
                        for key, value in sortedDict.items():
                            count = count + 1
                            if count == 10:
                                break
                            elif value != 1:
                                embed.add_field(name=f'#{count}',
                                                value=f"{key} - {value} times",
                                                inline=False)
                            else:
                                embed.add_field(name=count,
                                                value=f"{key} - {value} time",
                                                inline=False)
                        break
                    await ctx.send(embed=embed)
            except:
                embed = Embed(
                    title="Error",
                    description="This user hasn't sent any messages.")
                await ctx.send(embed=embed)
        else:
            embed = Embed(title="Error",
                          description="You've entered an incorrect argument.")
            await ctx.send(embed=embed)
    elif type == "server":
        if arg == "":  # sending most sent words in server
            with open('data.json', 'r', encoding='utf8') as file:
                data = json.load(file)
                guildDict = data[guildid]
                serverDict = dict()
                for a in dict(guildDict).keys():
                    for key, value in dict(data[guildid][a]).items():
                        key = str(key)
                        keystring = f"\'{key}\'"
                        value = int(value)
                        if str(serverDict) != '{}':
                            if keystring in str(serverDict.keys()):
                                serverDict[key] = serverDict[key] + value
                            else:
                                serverDict[key] = value
                        else:
                            serverDict[key] = value
                sortedDict = dict(
                    sorted(serverDict.items(),
                           key=lambda kv: kv[1],
                           reverse=True))
                count = -1
                embed = Embed(title=f"10 most used words in this server")
                while True:
                    for key, value in sortedDict.items():
                        count = count + 1
                        if count == 10:
                            break
                        elif value != 1:
                            embed.add_field(name=f'#{count + 1}',
                                            value=f"{key} - {value} times",
                                            inline=False)
                        else:
                            embed.add_field(name=f'#{count + 1}',
                                            value=f"{key} - {value} time",
                                            inline=False)
                    break
                await ctx.send(embed=embed)
        
        elif arg != "":  # sending amount of times people have said a specific word, with who has said it6
            with open('data.json', 'r', encoding='utf8') as file:
                data = json.load(file)
                guildDict = data[guildid]
                serverDict = dict()
                for a in guildDict.keys():
                    for key, value in data[guildid][a].items():
                        if key == arg:
                            serverDict[a] = value
                sortedDict = dict(
                    sorted(serverDict.items(), key=lambda kv: kv[1], reverse=True))
            
            count = -1
            embed = Embed(title=f"How many times has the word '{arg}' been said in {guildname}?")
            while True:
                for key, value in sortedDict.items():
                    count = count + 1
                    if count == 10:
                        break
                    elif value != 1:
                        embed.add_field(name=f'#{count + 1}',
                                        value=f"<@{key}> - {value} times",
                                        inline=False)
                    else:
                        embed.add_field(name=f'#{count + 1}',
                                        value=f"<@{key}> - {value} time",
                                        inline=False)
                break
            await ctx.send(embed=embed)

    else:
        embed = Embed(title="Error", description="You've entered an incorrect argument.")
        await ctx.send(embed=embed)


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
            msg1 = urllib.parse.quote(f"{message.author.name}#{message.author.discriminator} - {msgcontent}\n{files}")
        except:
            msg1 = urllib.parse.quote(f"{message.author.name}#{message.author.discriminator} - {msgcontent}")
        
        if replymsg != "":
            msg2 = urllib.parse.quote(f"Replying to: {replymsg}")
            requests.get(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg2}\n{msg1}")
        else:
            requests.get(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={msg1}")

    testsplit = '1'
    try:
        testsplit = msgcontent.split()[0]
    except:
        pass
    if testsplit != "!lb" and "''''" not in testsplit:
        userid = str(message.author.id)
        guildid = str(message.guild.id)
        message.content = message.content.split()
        if message.author != bot.user:
            with open('data.json', 'r', encoding='utf8') as file:
                if file.readlines() == []:
                    with open('data.json', 'w', encoding='utf8') as writing:
                        writing.write("{}")
            with open('data.json', 'r', encoding='utf8') as file:
                try:
                    data = json.load(file)
                except:
                    data = {}
                for i in message.content:
                    if i not in normal_words:
                        i = i.lower()
                        try:
                            data[guildid][userid][
                                i] = data[guildid][userid][i] + 1
                        except:
                            try:
                                data[guildid][userid][i] = 1
                            except:
                                try:
                                    data[guildid][userid] = {}
                                    data[guildid][userid][i] = 1
                                except:
                                    data[guildid] = {}
                                    data[guildid][userid] = {}
                                    data[guildid][userid][i] = 1
            os.remove('data.json')
            with open('data.json', 'w', encoding='utf8') as file:
                file.write(json.dumps(data, indent=4, sort_keys=True))


@bot.event
async def on_ready():
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')
    telegram_check.start()


r = requests.get(f"https://api.telegram.org/bot{telegram_token}/getUpdates?offset=-1")
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
