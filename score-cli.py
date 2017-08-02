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
    print(event['competitions'][0]['competitors'][0]['team']['abbreviation'])
    print(event['competitions'][0]['competitors'][1]['team']['abbreviation'])



aRequest = request.urlopen(
    'http://cdn.espn.com/core/mlb/scoreboard?xhr=1&render=true&' +
    'device=desktop&country=us&lang=en&region=us&site=espn&' +
    'edition-host=espn.com&site-type=full')
j = json.loads(aRequest.read().decode('utf-8'))

co = j['content']
group = co['sbGroup']
data = co['sbData']
events = data['events']
e = events[0]
c = e['competitions'][0]
types = [str, bool, int]
popTypes(c, types)
c.pop('notes')
c.pop('leaders')
c.pop('broadcasts')
c.pop('geoBroadcasts')

teams = c['competitors']  # This is a list of both teams
t = teams[0]
t.pop('probables')
t.pop('uid')
t.pop('id')
t.pop('type')
t.pop('order')

# figure out what t['order'] is


for e in events:
    process(e)


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
