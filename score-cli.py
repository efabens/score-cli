from urllib import request
import json


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
    event_info = []
    # top line
    game_description = event['status']['type']['description']
    if game_description in ['Delayed', 'Final']:
        game_detail = game_description + "/" + str(event['status']['period'])
    else:
        game_detail = event['status']['type']['detail']

    if event['status']['type']['state'] != 'pre':
        game_detail = add_whitespace(game_detail, 14) + "R  H  E"

    teams = event['competitions'][0]['competitors']
    away = teams[1]
    home = teams[0]
    print(game_detail)
    print(process_team(away))
    print(process_team(home))
    print()
    event_info.append(game_detail)
    event_info.append(process_team(away))
    event_info.append(process_team(home))
    return event_info


def process_team(team):
    t = add_whitespace(team['team']['name'], 14)
    try:
        runs = add_whitespace(str(team['score']), 3)
        hits = add_whitespace(str(team['hits']), 3)
        errors = add_whitespace(str(team['errors']), 3)
        return t + runs + hits + errors
    except KeyError:
        return t


# If the string is longer than length nothing is added
def add_whitespace(string, length):
    return string + ((length - len(string)) * " ")


aRequest = request.urlopen(
    'http://cdn.espn.com/core/mlb/scoreboard?xhr=1&render=true&' +
    'device=desktop&country=us&lang=en&region=us&site=espn&' +
    'edition-host=espn.com&site-type=full')
j = json.loads(aRequest.read().decode('utf-8'))

co = j['content']
group = co['sbGroup']
data = co['sbData']
events = data['events']
e = events[8]
c = e['competitions'][0]
types = [str, bool, int]


teams = c['competitors']  # This is a list of both teams
t = teams[0]
t.pop('probables')
t.pop('uid')
t.pop('id')
t.pop('type')
t.pop('order')

# figure out what t['order'] is

events = sorted(events, key=lambda x: x['competitions'][0]['status']['type']['state'])
events_to_print = []
for e in events:
    events_to_print.append(process(e))


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
