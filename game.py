from dateutil.parser import *
from webcolors import hex_to_rgb


class Game:
    def __init__(self, event):
        self.description = event['status']['type']['description']
        self.period = event['status']['period']
        c = event['competitions'][0]
        self.homeTeam = Team(c['competitors'][0])
        self.awayTeam = Team(c['competitors'][1])
        self.state = event['status']['type']['state']
        self.detail = event['status']['type']['detail']
        self.venue = c['venue']['fullName']
        self.startDate = c['startDate']
        self.date = (
            parse(event['date']).astimezone()
            .strftime('%a %b %d, at %I:%M %p'))
        self.hasOdds = False
        sit = c.get('situation', {})
        self.outs = sit.get('outs', 0)
        self.balls = sit.get('balls', 0)
        self.strikes = sit.get('strikes', 0)
        self.firstBase = sit.get('onFirst', False)
        self.secondBase = sit.get('onSecond', False)
        self.thirdBase = sit.get('onThird', False)
        if 'odds' in c:
            odds = c['odds'][0]
            self.hasOdds = True
            self.moneyline = odds['details']
            self.overUnder = odds['overUnder']

    def __str__(self):
        return "\n".join([str(i) for i in vars(Game)])


class Team:
    ENDC = '\033[0m'

    def __init__(self, team):
        self.name = team['team']['name']
        self.abbrev = team['team']['abbreviation']
        self.displayName = team['team']['displayName']
        self.color = team['team']['color']
        self.alternateColor = team['team']['alternateColor']
        self.runs = team.get('score', None)
        self.hits = team.get('hits', None)
        self.errors = team.get('errors', None)
        self.record = next(
            filter(
                lambda x: x['type'] == 'total', team['records']))['summary']

    def custom_text_color(self, tup):
        return (
            '\033[38;2;' +
            str(tup[0]) + ";" +
            str(tup[1]) + ";" +
            str(tup[2]) + 'm')

    def colorful_name(self):
        color = hex_to_rgb("#" + self.color)
        alt = hex_to_rgb("#" + self.alternateColor)

        return self.custom_text_color(color) + self.name + self.ENDC


