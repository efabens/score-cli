from game import Game, Team
from utility import custom_background, custom_text_color, ENDC


class MLBGame(Game):
    def __init__(self, event):
        Game.__init__(self, event)
        self.homeTeam = MLBTeam(self.c['competitors'][0])
        self.awayTeam = MLBTeam(self.c['competitors'][1])
        sit = self.c.get('situation', {})
        self.outs = sit.get('outs', 0)
        self.balls = sit.get('balls', 0)
        self.strikes = sit.get('strikes', 0)
        self.firstBase = sit.get('onFirst', False)
        self.secondBase = sit.get('onSecond', False)
        self.thirdBase = sit.get('onThird', False)
        self.link = f'espn.com/mlb/game?gameId={event["id"]}'
        if self.hasOdds:
            self.moneyline = self.odds[0].get('details', " ")
            self.overUnder = self.odds[0].get('overUnder', " ")


class MLBTeam(Team):
    def __init__(self, team):
        Team.__init__(self, team)
        self.runs = team.get('score', None)
        self.hits = team.get('hits', None)
        self.errors = team.get('errors', None)
        self.record = next(
            filter(
                lambda x: x['type'] == 'total', team['records']))['summary']
        self.division = self.get_league(self.abbrev)

    def colorful_name(self):
        color = self.color
        alt = self.alternateColor
        return (
            custom_text_color(color) + custom_background(alt) +
            self.name + ENDC)

    def get_colors(self):
        color1 = Team.get_colors(self)
        mlb_colors = {
            "OAK": {"alt": (0, 72, 58), "color": (255, 190, 0)},
            "HOU": {"alt": (255, 127, 0), "color": (7, 40, 84)},
            "TOR": {"alt": (29, 45, 92), "color": (0, 105, 172)},
            "SD": {"alt": (179, 163, 105), "color": (0, 29, 68)},
            "PHI": {"alt": (40, 72, 152), "color": (190, 0, 17)},
            "LAA": {"alt": (186, 3, 46), "color": (255, 255, 255)},
            "LAD": {"alt": (162, 170, 173), "color": (0, 51, 127)},
            "DET": {"alt": (250, 70, 20), "color": (12, 35, 64)},
            "NYY": {"alt": (196, 206, 212), "color": (1, 23, 57)},
            "TEX": {"alt": (192, 17, 31), "color": (0, 56, 121)},
            "CHC": {"alt": (0, 65, 125), "color": (200, 16, 46)},
            "CIN": {"alt": (255, 255, 255), "color": (196, 20, 34)},
            "NYM": {"alt": (0, 45, 112), "color": (252, 76, 0)},
            "KC": {"alt": (122, 178, 221), "color": (0, 59, 114)},
            "WSH": {"alt": (186, 18, 43), "color": (20, 34, 90)},
            "STL": {"alt": (196, 30, 58), "color": (255, 255, 255)},
            "ATL": {"alt": (0, 40, 85), "color": (186, 12, 47)},
            "CLE": {"alt": (12, 35, 64), "color": (213, 0, 50)},
            "MIL": {"alt": (196, 149, 59), "color": (1, 33, 67)},
            "MIN": {"alt": (4, 36, 98), "color": (255, 255, 255)},
            "COL": {"alt": (36, 19, 94), "color": (202, 205, 205)},
            "MIA": {"alt": (249, 66, 59), "color": (4, 130, 204)},
            "SF": {"alt": (0, 0, 0), "color": (251, 91, 31)},
            "CHW": {"alt": (220, 221, 223), "color": (0, 0, 0)},
            "TB": {"alt": (143, 188, 230), "color": (0, 36, 84)},
            "BOS": {"alt": (0, 34, 68), "color": (198, 12, 48)},
            "ARI": {"alt": (0, 0, 0), "color": (167, 25, 48)},
            "BAL": {"alt": (252, 76, 0), "color": (0, 0, 0)},
            "PIT": {"alt": (255, 199, 43), "color": (0, 0, 0)},
            "SEA": {"alt": (28, 139, 133), "color": (0, 49, 102)}
        }
        color1.update(mlb_colors)
        return color1

    def get_league(self, name):
        leagues = {
            "BAL": ["american", "east"],
            "BOS": ["american", "east"],
            "NYY": ["american", "east"],
            "TB": ["american", "east"],
            "TOR": ["american", "east"],
            "ATL": ["national", "east"],
            "MIA": ["national", "east"],
            "NYM": ["national", "east"],
            "PHI": ["national", "east"],
            "WSH": ["national", "east"],
            "CHW": ["american", "central"],
            "CLE": ["american", "central"],
            "DET": ["american", "central"],
            "KC": ["american", "central"],
            "MIN": ["american", "central"],
            "CHC": ["national", "central"],
            "CIN": ["national", "central"],
            "MIL": ["national", "central"],
            "PIT": ["national", "central"],
            "STL": ["national", "central"],
            "ARI": ["national", "west"],
            "COL": ["national", "west"],
            "LAD": ["national", "west"],
            "SD": ["national", "west"],
            "SF": ["national", "west"],
            "HOU": ["american", "west"],
            "LAA": ["american", "west"],
            "OAK": ["american", "west"],
            "SEA": ["american", "west"],
            "TEX": ["american", "west"]
        }
        return leagues[name]
