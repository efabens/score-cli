from game import Game, Team
import os
import json
from utility import custom_background, custom_text_color, ENDC


class SoccerGame(Game):
    def __init__(self, event, config: dict):
        Game.__init__(self, event)
        self.homeTeam = SoccerTeam(self.c['competitors'][0], config)
        self.awayTeam = SoccerTeam(self.c['competitors'][1], config)
        self.link = 'espnfc.us/match?gameid=' + event['id']
        if self.hasOdds:
            self.awayOdds = self.odds[0]['awayTeamOdds']['summary']
            self.homeOdds = self.odds[0]['homeTeamOdds']['summary']
            self.drawOdds = self.odds[0]['drawOdds']['summary']


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
                int(colors['alt'][i:i+2], 16) for i in (0, 2, 4))
            self.color = tuple(
                int(colors['color'][i:i+2], 16) for i in (0, 2, 4))
        elif (color and alt) and color != alt:
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
