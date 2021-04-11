from game import Game, Team
from utility import custom_text_color, custom_background, ENDC


class BasketballGame(Game):
    def __init__(self, event, config: dict):
        Game.__init__(self, event)
        self.homeTeam = BasketballTeam(self.c['competitors'][0], config)
        self.awayTeam = BasketballTeam(self.c['competitors'][1], config)
        self.link = f'espn.com/nba/game?gameId={event["id"]}'
        if self.hasOdds:
            self.moneyline = self.odds[0].get('details', " ")
            self.overUnder = self.odds[0].get('overUnder', " ")


class BasketballTeam(Team):
    def __init__(self, team, config: dict):
        Team.__init__(self, team)
        self.score = team.get('score', None)
        self.winner = team.get('winner', False)
        color = team['team'].get("color", False)
        alt = team['team'].get("alternateColor", False)
        custom = config.get("colors", {}).get("nba", {})
        if self.name in custom:
            colors = custom[self.name]
            self.alternateColor = tuple(
                int(colors['background'][i:i+2], 16) for i in (0, 2, 4))
            self.color = tuple(
                int(colors['text-color'][i:i+2], 16) for i in (0, 2, 4))
        elif (color and alt) and color != alt:
            config["colors"]["nba"][self.name] = {
                "background": alt, "text-color": color}
            self.alternateColor = tuple(
                int(color[i:i+2], 16) for i in (0, 2, 4))
            self.color = tuple(int(alt[i:i+2], 16) for i in (0, 2, 4))
        else:
            print(f"No color for {self.name}")

    def colorful_name(self):
        color = self.color
        alt = self.alternateColor
        return (
            custom_text_color(color) + custom_background(alt) +
            self.name + ENDC)
