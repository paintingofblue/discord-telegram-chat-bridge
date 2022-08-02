# Discord to Telegram bridge
File to bridge chat between Discord and Telegram. This allows users to send messages in a server, and for the message to be sent in a Telegram group.

# To-do
* Add Telegram to Discord
* Add the current channel in the message

# Installation

Open your telegram client and start a chat with [BotFather](https://t.me/BotFather). Send the message “/newbot” (no quotes) and follow the instructions.

![image](https://user-images.githubusercontent.com/90877067/182313481-fa70b777-c46f-4d59-8ddb-3dd55856d32d.png)

Upon following the instructions, BotFather will send you your bot token. 

![image](https://user-images.githubusercontent.com/90877067/182313860-72051436-a77c-4979-9d9e-324a6677fef8.png)

Send the message “/mybots” (no quotes), and select your bot. Click Bot Settings, Group Privacy, and make sure that option is disabled.
Upon doing this, you are free to invite your bot to your group.

![image](https://user-images.githubusercontent.com/90877067/182314225-05fdab18-9bbd-4a95-b87d-81a86117cf0c.png)

Once finished the above steps, make a POST request to [this link](https://api.telegram.org/bot<token>/getUpdates).
Replace <token> with the token BotFather provided you with, otherwise it won't work.

Making the request with [Hoppscotch](https://hoppscotch.io/) provided me with this (Note: I'm blurring out information I don't want public. Your response body will look different to mine.)
Make sure to note down the ID in the chat object.

![image](https://user-images.githubusercontent.com/90877067/182315491-7aedc897-a961-474c-9672-6293e80ea386.png)

Open the .env file provided, and replace the following values:
* Token - Your discord bot token
* telegram_token - Your telegram bot token sent by BotFather
* chatid - The ID you just noted down from the POST request you made

Run main.py, and it should now be listening for any messages sent in the server your bot is in.
