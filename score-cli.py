from datetime import datetime
from urllib import request
import json
from mlbgame import MLBGame
from utility import add_whitespace, print_events
from argparse import ArgumentParser


def process(game1):

    event_info = []
    # top line
    if game1.description in ['Delayed', 'Final']:
        game_detail = game1.description + "/" + str(game1.period)
    else:
        game_detail = game1.detail

    mid_line = process_team(game1.awayTeam, game1.state)
    bottom_line = process_team(game1.homeTeam, game1.state)

    if game1.state != 'pre':
        game_detail = add_whitespace(game_detail, 14) + "R  H  E  "
    else:
        game_detail = game1.date

    if game1.hasOdds:
        if game1.awayTeam.abbrev in game1.moneyline:
            mid_line, bottom_line = process_odds(mid_line, bottom_line, game1)

        elif game1.homeTeam.abbrev in game1.moneyline:
            bottom_line, mid_line = process_odds(bottom_line, mid_line, game1)

        elif game1.moneyline == 'EVEN':
            mid_line, bottom_line = process_odds(mid_line, bottom_line, game1)
        elif game1.moneyline == ' ':
            mid_line = add_whitespace(
                mid_line, 23, base=line_length(mid_line, game1.awayTeam))
            bottom_line = add_whitespace(
                bottom_line, 23, base=line_length(bottom_line, game1.homeTeam))

    top_line = add_whitespace(game_detail, 23)

    top_line, mid_line, bottom_line = ball_strike_out(
        top_line, mid_line, bottom_line, game1)

    top_line, mid_line, bottom_line = bases_loaded(
        top_line, mid_line, bottom_line, game1)

    event_info.append(top_line)
    event_info.append(mid_line)
    event_info.append(bottom_line)
    link = add_whitespace(game1.link, 36)
    event_info.append(link)
    return event_info


def line_length(line, team):
    return " " * (len(line)-len(team.colorful_name())+len(team.name))


def ball_strike_out(top, mid, bottom, game):
    top = (
        top + "  B:" + (u"\u25CF" * game.balls) +
        (u"\u25CB" * (4 - game.balls)))
    mid = (
        mid + "  S:" +
        u"\u25CF" * game.strikes + u"\u25CB" * (3 - game.strikes) + " ")
    bottom = (
        bottom + "  O:" + u"\u25CF" * game.outs + u"\u25CB" * (3 - game.outs) +
        " ")

    return top, mid, bottom


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
    if game.moneyline == 'EVEN':
        favorite = favorite + add_whitespace(game.moneyline, 9)
    else:
        favorite = favorite + add_whitespace(game.moneyline[3:].strip(), 9)
    dog = dog + add_whitespace("O/U:" + str(game.overUnder), 9)
    return favorite, dog


def process_team(team, state):
    t = add_whitespace(team.colorful_name(), 14, base=team.name)
    if state != "pre":
        runs = add_whitespace(str(team.runs), 3)
        hits = add_whitespace(str(team.hits), 3)
        errors = add_whitespace(str(team.errors), 3)
        return t + runs + hits + errors
    else:
        return t


def filter_team(leagues, divisions, away, home, name):
    if not leagues and not divisions and not name:
        return True
    filterHome = True
    filterAway = True
    if leagues:
        filterAway = away.division[0] in leagues
        filterHome = home.division[0] in leagues

    if divisions:
        filterAway = away.division[1] in divisions and filterAway
        filterHome = home.division[1] in divisions and filterHome

    nameMatch = True
    if name:
        nameMatch = name.lower() in (home.name + home.abbrev +
                                     home.shortDisplayName).lower() or name.lower() in (away.name + away.abbrev + away.shortDisplayName).lower()
    return (filterHome or filterAway) and nameMatch


def print_standings(args: str) -> None:
    # Available options 'd' <- division, 'w' <- wildcard, 'l' <- league,  'm' <- mlb
    print(args)


def print_scores(args: str) -> None:
    aRequest = request.urlopen(
        'http://cdn.espn.com/core/' + to_grab +
        '/scoreboard?xhr=1&render=true&' +
        'device=desktop&country=us&lang=en&region=us&site=espn&' +
        'edition-host=espn.com&site-type=full&date=' +
        datetime.now().strftime('%Y%m%d'))
    rawJson = json.loads(aRequest.read().decode('utf-8'))

    co = rawJson['content']
    group = co['sbGroup']
    data = co['sbData']
    events = data['events']

    events = sorted(
        events, key=lambda x: x['competitions'][0]['status']['type']['state'])
    events_to_print = []
    for e in events:
        game = MLBGame(e)
        if filter_team(args.leagues, args.divisions, game.awayTeam, game.homeTeam, args.teamName):
            events_to_print.append(process(game))

    print_events(events_to_print, 3)


if __name__ == '__main__':
    parser = ArgumentParser(
        description="prints out mlb scores. All data sourced from espn.com")
    parser.add_argument('-a', '--american', dest="leagues", action='append_const', const="american",
                        help="Display American League")
    parser.add_argument('-n', '--national', dest="leagues", action='append_const', const="national",
                        help="Display National League")
    parser.add_argument('-e', '--east', dest="divisions", action='append_const', const="east",
                        help="Display Eastern Division, for both leagues if no league flag passed")
    parser.add_argument('-c', '--central', dest="divisions", action='append_const', const="central",
                        help="Display Eastern Division, for both leagues if no league flag passed")
    parser.add_argument('-w', '--west', dest="divisions", action='append_const', const="west",
                        help="Display Eastern Division, for both leagues if no league flag passed")

    parser.add_argument('-s', "--search", dest="teamName", default="",
                        help="Returns teams where a team name matches the provided value")
    parser.add_argument("-S", "--standings", dest="standings", nargs="?",
                        const='d', action="store", help="Returns standings")

    args = parser.parse_args()
    to_grab = 'mlb'
    if args.standings:
        print_standings(args.standings)
    else:
        print_scores(args)

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
