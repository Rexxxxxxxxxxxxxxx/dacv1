import old_auto
import new_auto
import discord
import time
from datetime import datetime
import random
import asyncio
import yaml


with open('config/config.yml', 'r') as config:
    c = yaml.safe_load(config)
    token = c['token']
    bot = c['bot']
    prefix = c['prefix']

async def unverif(message, content):
    try:
        await message.delete()
    except:
        pass
    check = new_auto.ratelimit()
    if "429" in str(check[0]):
        await message.channel.send("We are currently ratelimited. Please wait " + str(round(check[1]['retry_after'])) + " seconds.")
        time.sleep(int(round(check[1]['retry_after'])))
    else:
        await message.channel.send("Creating " + str(content[1]) + " *verified* accounts.\nEstimated time: " + str(int(content[1]) * 2.5) + " minutes.")
    start_cmd_time = datetime.now()
    i = 1
    for _ in range(int(content[1])):
        start_gen_time = datetime.now()
        setting = old_auto.settings()
        proxy = old_auto.get_proxys('config/proxies.txt')
        email = old_auto.emails()
        old_auto.browser(setting[0], setting[1], setting[2], setting[3], email, proxy)

        result = old_auto.gettoken(setting[0], setting[1], email)
        print("result: " + str(result))
        end_gen_time = datetime.now()
        gen_time = end_gen_time - start_gen_time
       # old_auto.resend(email, setting[1], str(result))
        await message.channel.send("__**Account #" + str(i) + "'s Info:**__\nUsername: " + str(setting[0]) + "\nEmail: " + str(email) + "\nPassword: " + str(setting[1]) + "\nToken: " + str(result) + "\nTime to create account: " + str(round(gen_time.total_seconds(), 2)) + " seconds.")
        result = old_auto.ratelimit()
        if "429" in str(result[0]):
            await message.channel.send(str(i) + " iterations completed. Please wait " + str(round(result[1]['retry_after'])) + " seconds.")
            time.sleep(int(round(result[1]['retry_after'])))
        else:
            await message.channel.send("No ratelimit detected. Continuing.")

        i += 1
    await message.channel.send("Finished.")


async def verif(message, content):
    try:
        await message.delete()
    except:
        pass
    new_auto.checkers()
    proxy = new_auto.get_proxys()
    check = new_auto.ratelimit(proxy[0])
    if "429" in str(check[0]):
        await message.channel.send("We are currently ratelimited. Please wait " + str(round(check[1]['retry_after'])) + " seconds.")
        time.sleep(int(round(check[1]['retry_after'])))
    else:
        await message.channel.send("Creating " + str(content[1]) + " *verified* accounts.\nEstimated time: " + str(int(content[1]) * 1) + " minutes.")
    start_cmd_time = datetime.now()
    i = 1
    for _ in range(int(content[1])):
        start_gen_time = datetime.now()
        while True:
            try:
                setting = new_auto.settings()
                break
            except:
                pass
        email = new_auto.emails()
        token = new_auto.browser(setting[0], setting[1], setting[2], setting[3], email, proxy[0])
        end_gen_time = datetime.now()
        gen_time = end_gen_time - start_gen_time
        if token[0] != "Did not load page.":
            print(token)
            await message.channel.send("__**Account #" + str(i) + "'s Info:**__\nUsername: " + str(setting[0]) + "\nEmail: " + str(token[0]) + "\nPassword: " + str(setting[1]) + "\nToken: " + str(token[1]) + "\nTime to create account: " + str(round(gen_time.total_seconds(), 2)) + " seconds.")
            i += 1
        else:
            pass
        result = new_auto.ratelimit(proxy[0])
        if "429" in str(result[0]):
            await message.channel.send(str(i) + " iterations completed. Please wait " + str(round(result[1]['retry_after'])) + " seconds.")
            time.sleep(int(round(result[1]['retry_after'])))
        else:
            await message.channel.send("No ratelimit detected. Continuing.")


    await message.channel.send("Finished.")



async def grabtoken(message, content):
    email = content[1]
    password = content[2]
    result = old_auto.grabtoken(email, password)
    await message.channel.send("Token: " + str(result))


async def ratelimit(message):
    result = old_auto.ratelimit()
    if "429" in str(result[0]):
        await message.channel.send("Please wait " + str(round(result[1]['retry_after'])) + " seconds.")
    else:
        await message.channel.send("No ratelimit detected. You are free to continue.")







class MyClient(discord.Client):
    async def on_message(self, message):
        content = message.content.split(' ')
        if message.author == self.user:
            if content[0] == str(prefix) + "unverified":
                await unverif(message, content)
            elif content[0] == str(prefix) + "verified":
                await verif(message, content)
            elif content[0] == str(prefix) + "grabtoken":
                await grabtoken(message, content)
            elif content[0] == str(prefix) + "ratelimit":
                await ratelimit(message)

    async def on_connect(self):
        print(str(self.user.name))
        print(str(self.user.id))



client = MyClient()
client.run(token, bot=bot)