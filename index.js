/* -- Constants -- */
const { Utils } = require('./utils.js');
const { Client } = require('discord.js');
const client = new Client({ intents: 3276799 });
const axios = require('axios');
const ini = require('ini');
const fs = require('fs');
const config = ini.parse(fs.readFileSync("./config.ini", "utf-8"));

/* -- Variables -- */
let idDict = {}; // Formatted like {tgId: dcId}, used to give the bridge profile pictures & a name, or else it defaults to a Telegram icon and the username.
let update_id = null;

/* -- Events -- */
client.on('ready', async () => {
    /* -- Startup -- */
    await Utils.getTeleChannel().then(async (response) => {
        // Get the Discord channel name, and the Telegram channel name.
        let discName = client.channels.cache.get(config.discord.channelId).name;
        let teleName = response.result.title;

        console.log(`
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣿⡄
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⣿⡿⠿⠛⢙⣿⣿⠃
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣾⣿⣿⠿⠛⠋⠁⠀⠀⠀⣸⣿⣿⠀
    ⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⡿⠟⠛⠉⠀⠀⣠⣤⠞⠁⠀⠀⣿⣿⡇⠀
    ⠀⣴⣾⣿⣿⡿⠿⠛⠉⠀⠀⠀⢀⣠⣶⣿⠟⠁⠀⠀⠀⢸⣿⣿          Logged in as ${client.user.tag}.
    ⠸⣿⣿⣿⣧⣄⣀⠀⠀⣀⣴⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀⣼⣿⡿          Bridging messages between #${discName} and ${teleName}!
    ⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⢠⣿⣿⠇⠀⠀
    ⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡇⠀⣀⣄⡀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣠⣾⣿⣿⣿⣦⡀⠀⠀⣿⣿⡏⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⡿⠋⠈⠻⣿⣿⣦⣸⣿⣿⠁⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⠀⠀⠀⠀⠈⠻⣿⣿⣿⠏⠀⠀⠀⠀
        `);
    });

    /* -- Telegram loop handling -- */
    // Setting the update id to the latest message id, so that we don't get the most recent message once the bot is started/restarted.
    await axios.get(`https://api.telegram.org/bot${config.telegram.token}/getUpdates?offset=-1`).then(async (response) => {
        update_id = response.data.result[0].update_id;
    });

    // The loop that handles the Telegram messages and sends them to Discord.
    setInterval(async () => {
        await axios.get(`https://api.telegram.org/bot${config.telegram.token}/getUpdates?offset=-1`).then(async (response) => {
            response = response.data.result[0];
            if (response.update_id != update_id) {
                let discUser = "";
                let avatar = "https://cdn.discordapp.com/attachments/889397754458169385/1040525918508159036/166815113322072452.png"
                let name = response.message.from.username;
                let text = "";
                let path = "";
                update_id = response.update_id;

                if (response.message.from.id in idDict) {
                    discUser = await Utils.getUserInfo(idDict[response.message.from.id]);
                    avatar = `https://cdn.discordapp.com/avatars/${discUser.id}/${discUser.avatar}`;
                    name = discUser.username;
                }

                if ("photo" in response.message || "document" in response.message) {
                    if ("caption" in response.message) {
                        text = response.message.caption;
                    }
                    path = await Utils.getPhoto(response.message.photo[response.message.photo.length - 1].file_id);
                }

                if ("text" in response.message) {
                    text = response.message.text;
                }

                await Utils.sendDiscMsg(avatar, name, `${text}\n\n${path}`);
            }
        })
    }, 250); 
});

client.on('messageCreate', async (message) => {
    if (message.channel.id == config.discord.channelId && !message.author.bot && !message.author.system) {
        let attachments = "";
        message.attachments.forEach(Attachment => {
            attachments += Attachment.url + "\n";
        });

        if (message.reference == null) {
            await Utils.sendTeleMsg(`${message.author.username}#${message.author.discriminator} - ${message.cleanContent} ${attachments}`)
        } else {
            message.channel.messages.fetch(message.reference.messageId)
                .then(async repliedTo => {
                    await Utils.sendTeleMsg(`Replying to: ${repliedTo.author.username}#${repliedTo.author.discriminator} - ${repliedTo.content}\n${message.author.username}#${message.author.discriminator} - ${message.cleanContent} ${attachments}`)
                })
        }
    }
});

/* -- Login -- */
client.login(config.discord.token);