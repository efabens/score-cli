from dateutil.parser import *


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
        self.color = self.colors[self.abbrev]['color']
        self.alternateColor = self.colors[self.abbrev]['alt']
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

    def custom_background(self, tup):
        return (
            '\033[48;2;' +
            str(tup[0]) + ";" +
            str(tup[1]) + ";" +
            str(tup[2]) + 'm')

    def colorful_name(self):
        color = self.color
        alt = self.alternateColor
        return (
            self.custom_text_color(color) + self.custom_background(alt) +
            self.name + self.ENDC)

    colors = ({
  "OAK": {
    "alt": (0, 72, 58),
    "color": (255, 190, 0)
  },
  "HOU": {
    "alt": (255, 127, 0),
    "color": (7, 40, 84)
  },
  "TOR": {
    "alt": (29, 45, 92),
    "color": (0, 105, 172)
  },
  "SD": {
    "alt": (179, 163, 105),
    "color": (0, 29, 68)
  },
  "PHI": {
    "alt": (40, 72, 152),
    "color": (190, 0, 17)
  },
  "LAA": {
    "alt": (186, 3, 46),
    "color": (255, 255, 255)
  },
  "LAD": {
    "alt": (162, 170, 173),
    "color": (0, 51, 127)
  },
  "DET": {
    "alt": (250, 70, 20),
    "color": (12, 35, 64)
  },
  "NYY": {
    "alt": (196, 206, 212),
    "color": (1, 23, 57)
  },
  "TEX": {
    "alt": (192, 17, 31),
    "color": (0, 56, 121)
  },
  "CHC": {
    "alt": (0, 65, 125),
    "color": (200, 16, 46)
  },
  "CIN": {
    "alt": (255, 255, 255),
    "color": (196, 20, 34)
  },
  "NYM": {
    "alt": (0, 45, 112),
    "color": (252, 76, 0)
  },
  "KC": {
    "alt": (122, 178, 221),
    "color": (0, 59, 114)
  },
  "WSH": {
    "alt": (186, 18, 43),
    "color": (20, 34, 90)
  },
  "STL": {
    "alt": (196, 30, 58),
    "color": (255, 255, 255)
  },
  "ATL": {
    "alt": (0, 40, 85),
    "color": (186, 12, 47)
  },
  "CLE": {
    "alt": (12, 35, 64),
    "color": (213, 0, 50)
  },
  "MIL": {
    "alt": (196, 149, 59),
    "color": (1, 33, 67)
  },
  "MIN": {
    "alt": (4,36,98),
    "color": (255, 255, 255)
  },
  "COL": {
    "alt": (36, 19, 94),
    "color": (202, 205, 205)
  },
  "MIA": {
    "alt": (249, 66, 59),
    "color": (4, 130, 204)
  },
  "SF": {
    "alt": (0, 0, 0),
    "color": (251, 91, 31)
  },
  "CHW": {
    "alt": (220, 221, 223),
    "color": (0, 0, 0)
  },
  "TB": {
    "alt": (143, 188, 230),
    "color": (0, 36, 84)
  },
  "BOS": {
    "alt": (0, 34, 68),
    "color": (198, 12, 48)
  },
  "ARI": {
    "alt": (0, 0, 0),
    "color": (167, 25, 48)
  },
  "BAL": {
    "alt": (252, 76, 0),
    "color": (0, 0, 0)
  },
  "PIT": {
    "alt": (255, 199, 43),
    "color": (0, 0, 0)
  },
  "SEA": {
    "alt": (28, 139, 133),
    "color": (0, 49, 102)
  }
})
