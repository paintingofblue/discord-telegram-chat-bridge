/* -- Constants -- */
const { WebhookClient } = require('discord.js');
const webhookClient = new WebhookClient({ url: config.discord.webhookUrl });
const axios = require('axios');
const ini = require('ini');
const fs = require('fs');
const config = ini.parse(fs.readFileSync("./config.ini", "utf-8"));

/* -- Variables -- */
let dcToken = config.discord.token;
let tgToken = config.telegram.token;
let tgChatId = config.telegram.chatId;

/* -- Functions -- */
Utils = {
    /* -- Telegram -- */
    getTeleChannel: async function () {
        let response = await axios.post(`https://api.telegram.org/bot${tgToken}/getChat`, { chat_id: tgChatId });
        return response.data;
    },

    sendTeleMsg: async function (msg) {
        await axios.post(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
            chat_id: tgChatId,
            text: msg
        });
    },

    getPhoto: async function (id) {
        let path = await axios.get(`https://api.telegram.org/bot${tgToken}/getFile?file_id=${id}`);
        let newpath = `https://api.telegram.org/file/bot${tgToken}/${path.data.result.file_path}`;
        return newpath
    },

    /* -- Discord -- */
    getUserInfo: async function (id) {
        let response = await axios.get(`https://discord.com/api/v10/users/${id}`, {
            headers: {
                'Authorization': `Bot ${dcToken}`
            }
        });

        return response.data;
    },

    sendDiscMsg: async function (avatar, name, text) {
        try {
            await webhookClient.send({
                content: text,
                username: name,
                avatarURL: avatar
            });
        } catch (error) {
            void (0);
        }
    },
}

/* -- Exports -- */
module.exports = {
    Utils
}