from json import load
from utility import show_and_pop_all, loop, all_keys, pop_types, print_type


with open("mlb-overall.json", "r") as f:
    d = load(f)

data = d['standings']['entries']
