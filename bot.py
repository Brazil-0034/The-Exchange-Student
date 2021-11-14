import os
import sys

import discum
import openai
from dotenv import load_dotenv

import time
import random
import re


class ExcStd:

    load_dotenv()

    DISCORD_TOKEN = os.getenv('DS_TOKEN')
    OPAI_KEY = os.getenv('OPAI_KEY')

    bot = discum.Client(token=DISCORD_TOKEN, log=True)

    #
    # INIT DEFAULTS
    #

    active = True
    IS_PROCESSING = False

    bot.setAboutMe('HI! 👋')


    @bot.gateway.command
    def helloworld(resp):
        if resp.event.ready_supplemental:  # ready_supplemental is sent after ready
            user = bot.gateway.session.user
            print("Logged in as {}#{}".format(
                user['username'], user['discriminator']))
        if resp.event.message:
            m = resp.parsed.auto()
            processMessage(m)

            # print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))

    #
    # MESSAGE PROCESSING
    #


    lastHumanMsg = "Hello Jonah! How are you?"
    lastBotMsg = "I am Doing Well! Thanks."


    def getAdministrator(discrim=False):
        if (discrim):
            return os.getenv('ADMIN_DISCRIM')
        return os.getenv('ADMIN_NAME')


    def getBot(discrim=False):
        if (discrim):
            return os.getenv('BOT_DISCRIM')
        return os.getenv('BOT_NAME')


    def processMessage(msg):
        # because DMs are technically channels too
        guildID = msg['guild_id'] if 'guild_id' in msg else None
        channelID = msg['channel_id']
        username = msg['author']['username']
        discriminator = msg['author']['discriminator']
        content = msg['content']

        # avoid links and non english
        if "www" in content:
            return
        if "http" in content:
            return
        if "@" in content:
            return
        if not bool(re.match("[A-Za-z0-9 _.,!\"'/$]*", content, re.IGNORECASE)):
            return

        if (username != getBot() and discriminator != getBot(True)):
        # secret admin control panel
        # messaging the bot to deactivate will stop it when unmonitored
        # this way, you dont risk losing tokens while its unmonitored
            if (username == getAdmin() and discriminator == getAdmin(True)):
                if (content.lower() == "deactivate"):
                    bot.sendMessage(channelID, "Deactivated")
                    active = False
                    return
                elif (content.lower() == "activate"):
                    bot.sendMessage(channelID, "Activated")
                    active = True
                    return
            lastHumanMsg = content
            if (active == True):
                if (IS_PROCESSING == False):
                    APIGenerateResponse(content, channelID)
        else:
            lastBotMsg = content

    #
    # OPENAI INIT
    #


    openai.api_key = OPAI_KEY


    #
    # MSG RESPONSE
    #


    def APIGenerateResponse(newInput, id):
        time.sleep(random.randint(1, 3))
        IS_PROCESSING = True

        start_sequence = "\nJonah:"
        restart_sequence = "\nHuman: "

        start_prompt = "The following is a conversation with a boy named Jonah, who is an exchange student. Jonah is helpful, creative, clever, and very friendly.\n\nHuman: " + \
            lastHumanMsg + "\nJonah: " + lastBotMsg + "\nHuman: "

        bot.typingAction(id)

        print("Generating Response For: " + start_prompt + newInput + "\nJonah: ")

        result = ""
        while result == "":
            response = openai.Completion.create(
                engine="babbage",
                prompt=start_prompt + newInput + "\nJonah: ",
                temperature=0.7,
                max_tokens=32,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n", "Human:", "Jonah:"]
            )
            result = response.choices[0].text
            time.sleep(1)

        print(response)
        time.sleep(random.randint(2, 4))
        bot.sendMessage(id, result)
        IS_PROCESSING = False


    def setLastMsg(oftype, msg):
        if (oftype == "human"):
            lastHumanMsg = msg

    #
    # CONNECTION
    #


    bot.gateway.run(auto_reconnect=True)
