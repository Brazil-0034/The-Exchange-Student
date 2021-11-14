# The-Exchange-Student
Ever wondered what would happen if the Exchange Student joined your group chat?

## The Exchange Student
This project simulates a conversation between you and an exchange student. I made it for fun. It uses OpenAI's GPT-3 to create a realistic and contextual conversation. You can talk to it about anything. It fooled some of my friends in its realism.

## Backend
This project uses [Discord-SCUM](https://github.com/Merubokkusu/Discord-S.C.U.M/) to simulate a user, but can easily use [Nextcord](https://github.com/nextcord/nextcord) or [Discord.JS](https://github.com/discordjs/discord.js) or any other chat API wrapper.

## Setup
1. You will need access to the [OpenAI API Private Beta](http://beta.openai.com/)
2. Plug your tokens into the environment variables file
4. Have Fun (avg. token cost is ~$1.5/40 messages)

## Todo?
- Currently, the bot can only read the context from the past two conversations. I would like to increase this to 3 or more, but that would drastically increase API overhead and then cost as a result.
