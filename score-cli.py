from urllib import request
from time import time
import json
import os
from game import MLB_Game


def loop(a):
    for i in a.keys():
        print(i, type(a[i]))


def printType(a, types):
    for i in list(a.keys()):
        if type(a[i]) in types:
            print(i, a[i])


def popTypes(a, types):
    for i in list(a.keys()):
        if type(a[i]) in types:
            a.pop(i)


def process(event):
    game1 = MLB_Game(event)
    event_info = []
    # top line
    if game1.description in ['Delayed', 'Final']:
        game_detail = game1.description + "/" + str(game1.period)
    else:
        game_detail = game1.detail

    mid_line = process_team(game1.awayTeam)
    bottom_line = process_team(game1.homeTeam)

    if game1.state != 'pre':
        game_detail = add_whitespace(game_detail, 14) + "R  H  E  "
    else:
        game_detail = game1.date

    if game1.hasOdds:
        if game1.awayTeam.abbrev in game1.moneyline:
            mid_line, bottom_line = process_odds(mid_line, bottom_line, game1)

        elif game1.homeTeam.abbrev in game1.moneyline:
            bottom_line, mid_line = process_odds(bottom_line, mid_line, game1)

    top_line = add_whitespace(game_detail, 23)

    top_line, mid_line, bottom_line = ball_strike_out(
        top_line, mid_line, bottom_line, game1)

    top_line, mid_line, bottom_line = bases_loaded(
        top_line, mid_line, bottom_line, game1)

    event_info.append(top_line)
    event_info.append(mid_line)
    event_info.append(bottom_line)
    return event_info


def ball_strike_out(top, mid, bottom, game):
    top = (
        top + "  B:" + (u"\u25CF" * game.balls) +
        (u"\u25CB" * (4 - game.balls)))
    mid = (
        mid + "  S:" +
        u"\u25CF" * game.strikes + u"\u25CB" * (3 - game.strikes) + "  ")
    bottom = (
        bottom + "  O:" + u"\u25CF" * game.outs + u"\u25CB" * (3 - game.outs) +
        "  ")

    return (
        add_whitespace(top, 32),
        add_whitespace(mid, 32),
        add_whitespace(bottom, 32))


def bases_loaded(top, mid, bottom, game):
    top = top + "  " + on_base(game.secondBase) + "  "
    mid = mid + on_base(game.thirdBase) + "   " + on_base(game.firstBase)
    bottom = bottom + "  " + on_base(False) + "  "
    return top, mid, bottom


def on_base(boolean):
    if boolean:
        return u"\u25FC"
    else:
        return u"\u25FB"


def process_odds(favorite, dog, game):
    favorite = favorite + add_whitespace(game.moneyline[3:].strip(), 9)
    dog = dog + add_whitespace("O/U:" + str(game.overUnder), 9)
    return favorite, dog


def process_team(team):
    t = add_whitespace(team.colorful_name(), 14, base=team.name)
    if not(team.runs is None or team.hits is None or team.errors is None):
        runs = add_whitespace(str(team.runs), 3)
        hits = add_whitespace(str(team.hits), 3)
        errors = add_whitespace(str(team.errors), 3)
        return t + runs + hits + errors
    else:
        return t


# If the string is longer than length nothing is added
def add_whitespace(string, length, base=""):
    if base == "":
        base = string
    return string + ((length - len(base)) * " ")


if __name__ == '__main__':
    aRequest = request.urlopen(
        'http://cdn.espn.com/core/mlb/scoreboard?xhr=1&render=true&' +
        'device=desktop&country=us&lang=en&region=us&site=espn&' +
        'edition-host=espn.com&site-type=full')
    rawJson = json.loads(aRequest.read().decode('utf-8'))

    new_file = (os.path.realpath(__file__ + "/..") +
        '/files/' + str(int(time())) + '.json')

    with open(new_file, 'w+') as file:
        json.dump(rawJson, file)

    # with open("files/1501797864.json", 'r') as file:
    #     rawJson = json.load(file)

    co = rawJson['content']
    group = co['sbGroup']
    data = co['sbData']
    events = data['events']


    events = sorted(
        events, key=lambda x: x['competitions'][0]['status']['type']['state'])
    events_to_print = []
    for e in events:
        events_to_print.append(process(e))

    i = 0
    while i + 1 < len(events_to_print):
        for j in range(3):
            print("  |  ".join([i[j] for i in events_to_print[i:i + 2]]))
        print()
        i += 2
    if i < len(events_to_print):
        for j in range(3):
            print(events_to_print[i][j])

''' for baseball things to care about
 group has the page title which could be used as a header

  e['weather']
  c = e['competitions'][0]
  c['situation'] current state/ last play
  c['status'] inning
  c['venue'] location
  teams = c['competitors'] list of teams
  t = teams[0] teams are at 0 for home and 1 for away
  t['records'] maybe want
  t['errors'] errors
  t['hits'] hits
  t['score'] errors
  t['linescores'] inning by inning offensive scores per team
  t['team']['displayName'] full name with city
  t['team']['abbreviation'] Abbrev Name

  '''
