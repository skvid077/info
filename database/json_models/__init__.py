import json
import os


def get_path():
    return os.path.dirname(__file__)


def main():
    with open(file=os.path.join(os.path.dirname(__file__), 'friends.json'),
              mode='w',
              encoding='utf-8') as f:
        f.write(json.dumps({}))  # dict[int, dict[str, list[int]]]
    with open(file=os.path.join(os.path.dirname(__file__), 'variants.json'),
              mode='w',
              encoding='utf-8') as f:
        f.write(json.dumps({}))  # dict[int, list[int]]


if __name__ == '__main__':
    main()
