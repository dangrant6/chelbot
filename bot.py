import discord
from discord.ext import commands
import functions
import os
from dotenv import load_dotenv


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print('Bot is ready!')

    @client.command()
    async def hello(ctx):
        await ctx.send("Hello! I'm ChelBot. I can provide you with NHL scores and stat leaders.\nType !how for info on commands.")

    @client.command()
    async def how(ctx):
        await ctx.send("Use !nhl to view scores.\nUse !stats followed by the stat you want to to view stat leaders (ex. !stats points).")

    @client.command()
    async def scores(ctx):
        scores_message = await functions.scores(ctx)
        
    @client.command()
    async def standings(ctx):
        standings_message = await functions.standings(ctx)

    client.load_extension('functions')
    client.run(TOKEN)
