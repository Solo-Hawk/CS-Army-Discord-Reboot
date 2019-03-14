import json


def load_config():
    with open('core/configs.json') as r:
        return json.load(r)


def update_config(new_config):
    with open('core/configs.json', 'w') as w:
        json.dump(new_config, w)
