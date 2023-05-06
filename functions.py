import discord
from discord.ext import commands
import aiohttp
import bot

NHL_API = 'https://statsapi.web.nhl.com/api/v1'

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def scores(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{NHL_API}/schedule?expand=schedule.linescore') as response:
            data = await response.json()
            games = data['dates'][0]['games']
            if len(games) == 0:
                await ctx.send('No NHL games today.')
                return

            scores_message = 'Today\'s Scores:\n'
            for game in games:
                home_team = game['teams']['home']['team']['name']
                home_score = game['teams']['home']['score']
                away_team = game['teams']['away']['team']['name']
                away_score = game['teams']['away']['score']
                status = game['status']['detailedState']
                period = game['linescore']['currentPeriod']
                clock = game['linescore']['currentPeriodTimeRemaining']

                scores_message += f'{away_team} {away_score} - {home_team} {home_score} ({status}) - Period: {period} - Clock: {clock}\n'

            await ctx.send(scores_message)

@client.command()
async def standings(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{NHL_API}/standings') as response:
            data = await response.json()
            standings = data['records']

            standings_message = 'NHL Standings:\n\n'
            for record in standings:
                division_name = record['division']['name']
                standings_message += f'{division_name}\n'
                standings_message += '--------------------------\n'
                for team in record['teamRecords']:
                    team_name = team['team']['name']
                    points = team['points']
                    games_played = team['gamesPlayed']
                    wins = team['leagueRecord']['wins']
                    losses = team['leagueRecord']['losses']
                    ot_losses = team['leagueRecord']['ot']
                    standings_message += f'{team_name}: {points} points ({wins}-{losses}-{ot_losses}), {games_played} games played\n'
                standings_message += '\n'
    
    await ctx.send(standings_message)