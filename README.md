# Discord Telegram bridge

File to bridge chat between Discord and Telegram. This allows users to send messages & attatchments in a server, and for the message to also be sent in a Telegram group.

![image](https://user-images.githubusercontent.com/90877067/201297882-45093b37-9c65-4c4c-8742-9137bb097306.png)


## Supported

* Discord > Telegram (messages & attatchments)
* Telegram > Discord (messages & attatchments)

## Installation

Open your Telegram client and start a chat with [BotFather](https://t.me/BotFather). Send the message “/newbot” (no quotes) and follow the instructions.

![image](https://user-images.githubusercontent.com/90877067/182313481-fa70b777-c46f-4d59-8ddb-3dd55856d32d.png)

Upon following the instructions, BotFather will send you your bot token.

![image](https://user-images.githubusercontent.com/90877067/182313860-72051436-a77c-4979-9d9e-324a6677fef8.png)

Send the message “/mybots” (no quotes), and select your bot. Click Bot Settings, Group Privacy, and make sure that option is disabled.
Upon doing this, you are free to invite your bot to your group.

![image](https://user-images.githubusercontent.com/90877067/182314225-05fdab18-9bbd-4a95-b87d-81a86117cf0c.png)

Once finished the above steps, visit this link <https://api.telegram.org/botToken/getUpdates?offset=-1>.
Replace `Token` with the token BotFather provided you with, otherwise it won't work.

Making the request with [Hoppscotch](https://hoppscotch.io/) provided me with this (Note: I'm blurring some information out. Your response body will look different to mine.)
Make sure to note down the ID in the chat object.

![image](https://user-images.githubusercontent.com/90877067/182315491-7aedc897-a961-474c-9672-6293e80ea386.png)

Open the config.ini file provided, and replace the following values:

### Discord

* Token - Your Discord bot token
* Channel ID - The ID of the channel you want to bridge.
* Webhook URL - The webhook URL of the channel you want to bridge.

### Telegram

* Token - The token BotFather provided you with.
* Chat ID - The ID of the chat you noted down previously.

Run main.py, and it should now be listening for any messages sent in the server your bot is in.

Discord -> Telegram  |  Telegram -> Discord
:--------------------:|:---------------------:
![Sending a message in Discord](https://cdn.discordapp.com/attachments/889397754458169385/1040538516238651422/166815413825077623.png) | ![Sending a message in Telegram](https://cdn.discordapp.com/attachments/889397754458169385/1040538702012760104/166815418025119756.png)
![Seeing the message sent in Telegram](https://cdn.discordapp.com/attachments/889397754458169385/1040538516620312576/166815413825077623.png) | ![Seeing the message sent in Discord](https://cdn.discordapp.com/attachments/889397754458169385/1040538756555477002/166815419425133878.png)
