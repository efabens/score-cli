ENDC = '\033[0m'


def all_keys(a_map, whitespace=''):
    if type(a_map) == dict:
        for i in a_map.keys():
            print(whitespace + str(i))
            all_keys(a_map[i], whitespace + "   ")
    elif type(a_map) in [set, list]:
        for i in a_map:
            all_keys(i, whitespace + "")


def loop(a):
    for i in a.keys():
        print(i, type(a[i]))


def show_and_pop(the_map, key):
    print(the_map[key])
    print(type(the_map[key]))
    print(key)
    r = input()
    if r == 'y':
        the_map.pop(key)


def show_and_pop_all(the_map):
    for i in list(the_map.keys()):
        show_and_pop(the_map, i)


def print_type(a, types):
    for i in list(a.keys()):
        if type(a[i]) in types:
            print(i, a[i])


def pop_types(a, types):
    for i in list(a.keys()):
        if type(a[i]) in types:
            a.pop(i)


# If the string is longer than length nothing is added
def add_whitespace(string, length, base=""):
    if base == "":
        base = string
    return string + ((length - len(base)) * " ")


def custom_text_color(tup):
    return (
        '\033[38;2;' +
        str(tup[0]) + ";" +
        str(tup[1]) + ";" +
        str(tup[2]) + 'm')


def custom_background(tup):
    return (
        '\033[48;2;' +
        str(tup[0]) + ";" +
        str(tup[1]) + ";" +
        str(tup[2]) + 'm')


def print_events(events_to_print, width):
    bigeventlist = []
    for x, y in enumerate(events_to_print):
        if x % width == 0:
            small = []
            bigeventlist.append(small)
        small.append(y)

    for i in bigeventlist:
        for j in range(len(i[0])):
            print("  |  ".join([x[j] for x in i]))
        print()


def stringify_events(events_to_print, width):
    bigeventlist = []
    for x, y in enumerate(events_to_print):
        if x % width == 0:
            small = []
            bigeventlist.append(small)
        small.append(y)
    s = ""
    for i in bigeventlist:
        for j in range(len(i[0])):
            s = s+"  |  ".join([x[j] for x in i]) + "\n"

    return s


def ansi_to_html(to_convert: str):
    return to_convert.replace("\n", "<p>")
