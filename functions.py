import requests
import datetime
import json
import discord

class botFuncs:
    def __init__(self):
        self.NHLAPI = "http://statsapi.web.nhl.com/api/v1"
        self.SCHEDULE = "/schedule"

    def route(self, msg):

        msgarr = msg.split()

        msgarr.pop(0)

        if not msgarr:
            return None

        if msgarr[0].lower() == 'schedule':
            if len(msgarr) > 1:
                return self.getScheduleByDate(msgarr[1])
            else:
                return self.getDailySchedule()

    def getDailySchedule(self):

        result = requests.get(self.NHLAPI+self.SCHEDULE)
        data = result.json()
        try:
            test = data['dates'][0]['games']
            return self.formatSchedule(data)
        except:
            return self.getScheduleByDate('tomorrow')

        return "Error"

    def getScheduleByDate(self, date):
        print("getScheduleByDate entered")
        if date.lower() == 'tomorrow':
            x = datetime.datetime.now()
            print(x)
            print(x.hour)
            if int(x.hour) < 9:
                date = str(x).split()[0]
            else:
                date = str(x + datetime.timedelta(days=1)).split()[0]

        else:
            return "Future lookup currently only supports 'tomorrow'"

        print("Searching date:"+date)
        req = self.NHLAPI + self.SCHEDULE + '?date=' + date

        print(req)

        result = requests.get(req)

        data = result.json()

        return self.formatSchedule(data)

    def formatSchedule(self, data):

        thegoods = f"```js\nSchedule for {data['dates'][0]['date']}"

        for x in data['dates'][0]['games']:
            thegoods += '\n'
            thegoods += "Status: "  # + x['status']['abstractGameState']

            gamestatus = x['status']['abstractGameState']

            if gamestatus == 'Preview':
                thegoods += self.formatDate(x['gameDate'])
            elif gamestatus == 'Live':
                thegoods += 'Live '
            elif gamestatus == 'Final':
                thegoods += 'Final'
            else:
                thegoods += "Date/Status error"

            thegoods += "\tTeams: " + \
                x['teams']['home']['team']['name'] + " vs " + \
                x['teams']['away']['team']['name']
            if gamestatus != 'Preview':
                thegoods += "\tScore:\t" + \
                    str(x['teams']['home']['score']) + " : " + \
                    str(x['teams']['away']['score'])

        thegoods += "```"
        return thegoods

    def formatDate(self, date):

        date = date.split('T')[1]
        date = date.split(':')

        if int(date[0]) < 12:
            date[0] = str(int(date[0])+24)
        date[0] = str(int(date[0])-16)

        print(date)

        final = ''

        for x in date:
            if x == '0':
                x = '12'
            final += x + ':'

        final = final[0:len(final)-5]

        final = final + " ET"

        return final

    #Gets Standings Function
    def getStandings(ctx, division):
        base_url = 'https://statsapi.web.nhl.com/api/v1/standings'
        response = requests.get(base_url)
        standingsJSON = response.text
        nhlStandings = json.loads(standingsJSON)
        divisionName = {"Pacific", "Central",
                        "Atlantic", "Metropolitan"}

        print(divisionName[0])

        divisionNum = 3
        numTeams = len(nhlStandings['records'][divisionNum]['teamRecords'])
        x = 0
        myEmbed = discord.Embed(title=f"Standings For: ",
                                description=f" {nhlStandings['records'][divisionNum]['division']['name']} \n", color=0x00ff00)
        myEmbed.set_author(name=ctx.author.display_name,
                        url="https://www.nhl.com/", icon_url=ctx.author.avatar_url)
        myEmbed.set_thumbnail(
            url=f"https://www-league.nhlstatic.com/images/logos/league-dark/133-flat.svg")

        nhlStandings = nhlStandings['records'][divisionNum]['teamRecords']

        for x in range(numTeams):
            myEmbed.add_field(name=f"{x+1}. {nhlStandings[x]['team']['name']}", value=f" > Record [{nhlStandings[x]['gamesPlayed']}GP]: ({nhlStandings[x]['leagueRecord']['wins']}W - {nhlStandings[x]['leagueRecord']['losses']}L - {nhlStandings[x]['leagueRecord']['ot']}OT - {nhlStandings[x]['points']}P) \n > League Rank: {nhlStandings[x]['leagueRank']} \n > Streak: {nhlStandings[x]['streak']['streakCode']} \n > GA: {nhlStandings[x]['goalsAgainst']} - GF: {nhlStandings[x]['goalsScored']}  ", inline=False)

        return myEmbed
