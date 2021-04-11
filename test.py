from json import load
from utility import show_and_pop_all, loop, all_keys, pop_types, print_type


def print_pitch(event):
    loop(event)
    if event['isPitch']:
        details = event['details']
        pitchData = event['pitchData']
        print(details)
        print(
            f"({pitchData['coordinates']['x']},{pitchData['coordinates']['y']})")

    return event


with open("game-updates.json", "r") as f:
    data = load(f)

ld = data['liveData']
# loop(ld)
# This probably has everything needed to show the full 9 inning scores
# show_and_pop_all(ld['linescore'])

print("Plays")
plays = ld['plays']
# loop(plays)
# show_and_pop_all(plays)
# allPlays <class 'list'>
# currentPlay <class 'dict'>
# scoringPlays <class 'list'>
# playsByInning <class 'list'>

allplays = plays['allPlays']
oneplay = allplays[0]
lastplay = allplays[-1]
# print("One Play")
# loop(oneplay)

# events = oneplay['playEvents']
# loop(events[0])
# for i in events:
#     print("\nNext Play")
#     print_pitch(i)

current = plays['currentPlay']
show_and_pop_all(current)
for i in current['playEvents']:
    print_pitch(i)
