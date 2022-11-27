import os
import discord
import functions


TOKEN = ('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())
messagerouter = functions.botFuncs()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:2] == 'HB':
        result = messagerouter.route(message.content)
        if result:
            await message.channel.send(result)

client.run(TOKEN)
