from game import Game, Team
import os
from utility import custom_background, custom_text_color, ENDC


class SoccerGame(Game):
    def __init__(self, event, config: dict):
        Game.__init__(self, event)
        self.homeTeam = SoccerTeam(self.c['competitors'][0], config)
        self.awayTeam = SoccerTeam(self.c['competitors'][1], config)
        self.link = 'espn.com/soccer/match?gameId=' + event['id']
        if self.hasOdds:
            if 'awayTeamOdds' in self.odds[0]:
                away = self.odds[0]['awayTeamOdds']
                self.awayOdds = self.extractOdds(away)
                
            if 'homeTeamOdds' in self.odds[0]:
                home = self.odds[0]['homeTeamOdds']
                self.homeOdds = self.extractOdds(home)
            if 'drawOdds' in self.odds[0]:
                draw = self.odds[0]['drawOdds']
                self.drawOdds = self.extractOdds(draw)

    def extractOdds(self, odds: dict):
        if 'summary' in odds:
            return odds['summary']
        elif 'moneyLine' in odds:
            return odds['moneyLine']
        else:
            return ""


class SoccerTeam(Team):
    def __init__(self, team, config: dict):
        Team.__init__(self, team)
        self.score = team.get('score', None)
        self.winner = team.get('winner', False)
        color = team['team'].get("color", False)
        alt = team['team'].get("alternateColor", False)
        custom = config.get("colors", {}).get("soccer", {})
        if self.name in custom:
            colors = custom[self.name]
            self.alternateColor = tuple(
                int(colors['background'][i:i+2], 16) for i in (0, 2, 4))
            self.color = tuple(
                int(colors['text-color'][i:i+2], 16) for i in (0, 2, 4))
        elif (color and alt) and color != alt:
            config["colors"]["soccer"][self.name] = {
                "background": alt, "text-color": color}
            self.alternateColor = tuple(
                int(color[i:i+2], 16) for i in (0, 2, 4))
            self.color = tuple(int(alt[i:i+2], 16) for i in (0, 2, 4))

    def colorful_name(self):
        color = self.color
        alt = self.alternateColor
        return (
            custom_text_color(color) + custom_background(alt) +
            self.name + ENDC)

    # Potential things to include
'''
Team; last 5 form -> team['form']
'''
