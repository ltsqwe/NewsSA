import json


def print_json(json_dict):   # get dict
    print(json.dumps(json_dict, indent=4))


def pl(msg, show):
    if show:
        print(msg, end='')


def pld(show):
    if show:
        print('Done!')