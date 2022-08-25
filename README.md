# Discord to Telegram bridge
File to bridge chat between Discord and Telegram. This allows users to send messages & attatchments in a server, and for the message to also be sent in a Telegram group.

# Supported
* Discord > Telegram (messages & attatchments)
* Telegram > Discord (messages & attatchments)

# Installation

Open your Telegram client and start a chat with [BotFather](https://t.me/BotFather). Send the message “/newbot” (no quotes) and follow the instructions.

![image](https://user-images.githubusercontent.com/90877067/182313481-fa70b777-c46f-4d59-8ddb-3dd55856d32d.png)

Upon following the instructions, BotFather will send you your bot token. 

![image](https://user-images.githubusercontent.com/90877067/182313860-72051436-a77c-4979-9d9e-324a6677fef8.png)

Send the message “/mybots” (no quotes), and select your bot. Click Bot Settings, Group Privacy, and make sure that option is disabled.
Upon doing this, you are free to invite your bot to your group.

![image](https://user-images.githubusercontent.com/90877067/182314225-05fdab18-9bbd-4a95-b87d-81a86117cf0c.png)

Once finished the above steps, make a POST request to [this link](https://api.telegram.org/bot<token>/getUpdates).
Replace <token> with the token BotFather provided you with, otherwise it won't work.

Making the request with [Hoppscotch](https://hoppscotch.io/) provided me with this (Note: I'm blurring some information out. Your response body will look different to mine.)
Make sure to note down the ID in the chat object.

![image](https://user-images.githubusercontent.com/90877067/182315491-7aedc897-a961-474c-9672-6293e80ea386.png)

Open the .env file provided, and replace the following values:
* Token - Your Discord bot token
* telegram_token - Your Telegram bot token sent by BotFather
* chatid - The ID you just noted down from the POST request you made
* webhook - Make a discord webhook in your server

Run main.py, and it should now be listening for any messages sent in the server your bot is in.

![image](https://user-images.githubusercontent.com/90877067/182317046-73e925c4-8a11-4ff5-993e-7e3db9ef5a26.png)

![image](https://user-images.githubusercontent.com/90877067/182317079-0e74c1ee-10ab-4fd9-9540-1a1557b2cdee.png)
