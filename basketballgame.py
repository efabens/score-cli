from game import Game, Team
from utility import custom_text_color, custom_background, ENDC

class BasketballGame(Game):
    def __init__(self, event):
        Game.__init__(self, event)
        self.homeTeam = BasketballTeam(self.c['competitors'][0])
        self.awayTeam = BasketballTeam(self.c['competitors'][1])
        self.link = f'espn.com/nba/game?gameId={event["id"]}'
        if self.hasOdds:
            self.moneyline = self.odds[0].get('details', " ")
            self.overUnder = self.odds[0].get('overUnder', " ")


class BasketballTeam(Team):
    def __init__(self, team):
        Team.__init__(self, team)
        self.score = team.get('score', None)
        self.winner = team.get('winner', False)

    def colorful_name(self):
        color = self.color
        alt = self.alternateColor
        return (
                custom_text_color(color) + custom_background(alt) +
                self.name + ENDC)

    def get_colors(self):
        color1 = Team.get_colors(self)
        nba_colors = {
            "POR": {"alt": (224, 58, 62), "color": (6, 25, 34)},
            "PHI": {"alt": (237, 23, 76), "color": (0, 107, 182)},
            "TOR": {"alt": (117, 59, 189), "color": (138, 141, 143)},
            "DEN": {"alt": (255, 198, 39), "color": (13, 34, 64)}
        }
        color1.update(nba_colors)
        return color1
