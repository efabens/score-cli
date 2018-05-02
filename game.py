from dateutil.parser import parse
import json


class Game:
    def __init__(self, event):
        self.raw = event
        self.description = event['status']['type']['description']
        self.period = event['status']['period']
        self.state = event['status']['type']['state']
        self.detail = event['status']['type']['detail']
        self.c = event['competitions'][0]
        self.venue = self.c.get('venue', {'fullName': ''})['fullName']
        self.startDate = self.c['startDate']
        self.date = (
            parse(event['date']).astimezone()
            .strftime('%a %b %d, at %I:%M %p'))
        self.hasOdds = False
        if 'odds' in self.c:
            # with open('odds.json', 'w+') as file:
            #     json.dump(self.c['odds'], file)
            self.odds = self.c['odds']
            self.hasOdds = True

    def __str__(self):
        return "\n".join([str(i) for i in vars(Game)])


class Team:
    def __init__(self, team):
        self.name = team['team']['name']
        self.abbrev = team['team'].get('abbreviation', self.name)
        self.displayName = team['team']['displayName']
        self.shortDisplayName = team['team'].get('shortDisplayName')
        all_colors = self.get_colors()
        color_vals = all_colors.get(self.abbrev, all_colors['STANDARD'])
        self.color = color_vals['color']
        self.alternateColor = color_vals['alt']
        self.raw = team

    def get_colors(self):
        return {"STANDARD": {"alt": (0, 0, 0), "color": (255, 255, 255)}}

    def colorful_name(self):
        return self.name

    def __str__(self):
        return "\n".join([str(i) for i in vars(Team)])
