# Telegram Bot Configuration

In order to send messages to telegram you will need a Telegram Bot.

To create a Telegram bot and obtain the bot token and chat ID, you'll need to follow these steps:

1. Create a Telegram Bot:
    * Open the Telegram app and search for the "BotFather" (username: @BotFather).
    * Start a chat with BotFather and use the command "/newbot" to create a new bot.
    * Follow the instructions provided by BotFather to choose a name and username for your bot. d. Once the bot is
      created, BotFather will provide you with a unique API token. This token is your bot token, and you will need it to
      authenticate and interact with the Telegram Bot API.

2. Obtain your Chat ID:
    * Add your newly created bot to the desired Telegram chat or group where you want to receive messages.
    * Open a web browser and enter the following URL, replacing __[YourBotToken]__ with the token you received from
      BotFather: https://api.telegram.org/bot[YourBotToken]/getUpdates
    * You should see a JSON response that contains information about the most recent messages received by your bot.
    * Look for the "chat" object in the response, which contains details about the chat your bot is part of.
    * The "id" field within the "chat" object corresponds to the chat ID of the group or channel. Make note of this chat
      ID; you will need it to send messages to the chat.

Remember to keep your bot token and chat ID confidential and do not share them publicly or with unauthorized
individuals. With this information, you can use the Telegram Bot API to program your bot to send and receive messages in
your chat or group.