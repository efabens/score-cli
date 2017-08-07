import json
import os
from datetime import datetime
from urllib import request

from soccergame import SoccerGame
from utility import add_whitespace, custom_text_color, custom_background, ENDC, print_events


def process(game_event):
    game1 = SoccerGame(game_event)
    event_info = []
    # print(game1.description, game1.period, game1.state, game1.detail)
    # top line
    game_detail = game1.detail
    mid_line = process_team(game1.homeTeam, game1.state)
    bottom_line = process_team(game1.awayTeam, game1.state)
    link = add_whitespace(game1.link, 29)

    if game1.state != 'pre':
        top_line = add_whitespace(game_detail, 20) + "   Score "
    else:
        top_line = add_whitespace(game1.date, 29)

    event_info.append(top_line)
    event_info.append(mid_line)
    event_info.append(bottom_line)
    event_info.append(link)
    return event_info


def process_team(team, state):
    t = add_whitespace(team.colorful_name(), 26, base=team.name)

    if state != 'pre':

        if team.winner:
            score = add_whitespace(
                custom_background((255, 255, 255)) + custom_text_color((0, 0, 0)) + str(team.score) + ENDC, 3,
                base=str(team.score))
        else:
            score = add_whitespace(str(team.score), 3)
        return t + score
    else:
        return t + '   '

if __name__ == '__main__':
    to_grab = 'soccer'

    aRequest = request.urlopen(request.Request(
        'http://cdn.espn.com/core/' + to_grab +
        '/scoreboard?xhr=1&render=true&' +
        'device=desktop&country=us&lang=en&region=us&site=espn&' +
        'edition-host=espn.com&site-type=full&date=' +
        datetime.now().strftime('%Y%m%d'),
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)' +
                          ' Chrome/59.0.3071.115 Safari/537.36'}))
    rawJson = json.loads(aRequest.read().decode('utf-8'))

    co = rawJson['content']
    group = co['sbGroup']
    data = co['sbData']
    skores = data['scores']  # This is a list that has a value for each league
    league = skores[0]  # This is just one league which contains many events
    # and there are many leagues
    events = league['events']
    event = events[0]
    # events = data['events']

    config_file = (
        os.path.realpath(__file__ + "/..") +
        '/config.json')

    if os.path.isfile(config_file):
        with open(config_file, 'r+') as file:
            config = json.load(file)
    else:
        config = {}
    config_changes = False
    config_leagues = config.get('soccer_leagues', {})
    for i in skores:
        j = i['leagues'][0]
        midsize = j['midsizeName']
        if midsize not in config_leagues:
            config_changes = True
            print(print(j['name'], midsize))
            to_display = input("display: y/n ")
            to_display = to_display[0] == 'y'
            config_leagues[midsize] = (
                {'to_display': to_display, 'name': j['name']})
    if config_changes:
        config['soccer_leagues'] = config_leagues
        with open(config_file, 'w+') as file:
            json.dump(config, file, indent=4, sort_keys=True)

    if 'test' in config:
        print('test')

    to_print = [l for l in skores if config['soccer_leagues'][l['leagues'][0]['midsizeName']]['to_display']]
    for l in to_print:
        events_to_print = []
        events = sorted(
            l['events'], key=lambda x: x['competitions'][0]['status']['type']['state'])
        league_name = l['leagues'][0]['name']
        print(custom_background((255, 255, 255)) + custom_text_color((0, 0, 0)) + league_name + ENDC)
        for e in events:
            events_to_print.append(process(e))

        print_events(events_to_print, 3)



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
