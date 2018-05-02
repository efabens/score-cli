from game import Game, Team


class SoccerGame(Game):
    def __init__(self, event):
        Game.__init__(self, event)
        self.homeTeam = SoccerTeam(self.c['competitors'][0])
        self.awayTeam = SoccerTeam(self.c['competitors'][1])
        self.link = 'espnfc.us/match?gameid=' + event['id']
        if self.hasOdds:
            self.awayOdds = self.odds[0]['awayTeamOdds']['summary']
            self.homeOdds = self.odds[0]['homeTeamOdds']['summary']
            self.drawOdds = self.odds[0]['drawOdds']['summary']


class SoccerTeam(Team):
    def __init__(self, team):
        Team.__init__(self, team)
        self.score = team.get('score', None)
        self.winner = team.get('winner', False)

    def colorful_name(self):
        return self.name

# Potential things to include
'''
Team; last 5 form -> team['form']
'''