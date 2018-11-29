import json
import os
from datetime import datetime
from urllib import request

from basketballgame import BasketballGame
from utility import add_whitespace, custom_text_color, custom_background, ENDC, print_events, show_and_pop_all


def process(game_event):
    game1 = BasketballGame(game_event)
    event_info = []
    # print(game1.description, game1.period, game1.state, game1.detail)
    # top line
    game_detail = game1.detail
    mid_line = process_team(game1.homeTeam, game1.state)
    bottom_line = process_team(game1.awayTeam, game1.state)
    link = add_whitespace(game1.link, 36)

    if game1.state != 'pre':
        top_line = add_whitespace(game_detail, 27) + "   Score "
    else:
        top_line = add_whitespace(game1.date, 36)

    event_info.append(top_line)
    event_info.append(mid_line)
    event_info.append(bottom_line)
    event_info.append(link)
    return event_info


def process_team(team, state):
    t = add_whitespace(team.colorful_name(), 33, base=team.name)

    if state != 'pre':

        if team.winner:
            score = add_whitespace(
                custom_background(
                    (255, 255, 255)) + custom_text_color((0, 0, 0)) + str(team.score) + ENDC, 3,
                base=str(team.score))
        else:
            score = add_whitespace(str(team.score), 3)
        return t + score
    else:
        return t + '   '


if __name__ == '__main__':
    to_grab = 'nba'

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
    # skores = data['scores']  # This is a list that has a value for each league
    # league = skores[0]  # This is just one league which contains many events
    # # and there are many leagues
    # events = league['events']
    # event = events[0]
    events_to_print = data['events']
    [process(i) for i in events_to_print]

    print_events([process(i) for i in events_to_print], 2)


