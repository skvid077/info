import json


def main():
    with open(file='friends.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps({}))  # dict[int, dict[str, list[int]]]
    with open(file='variants.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps({}))  # dict[int, list[int]]


if __name__ == '__main__':
    main()
