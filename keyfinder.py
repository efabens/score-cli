def allKeys(a_map, whitespace=''):
    if type(a_map) == dict:
        for i in a_map.keys():
            print(whitespace + str(i))
            allKeys(a_map[i], whitespace + "   ")
    elif type(a_map) in [set, list]:
        for i in a_map:
            allKeys(i, whitespace + "")
