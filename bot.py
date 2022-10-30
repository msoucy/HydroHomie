#!/usr/bin/env python
from mastodon import Mastodon
from random import choice
from pprint import pprint
import os

masto = Mastodon(
    api_base_url='https://botsin.space',
    client_id="client_id.txt",
    access_token="access_token.txt"
)

def readFile(fn):
    with open(fn) as fi:
        lines = fi.readlines()
    return [line.strip()
            for line in lines
            if not line.startswith("#")]

if __name__ == '__main__':
    texts = readFile("hydro.txt")
    text = choice(texts)
    print("Tooting:", text)
    status_result = masto.status_post(text)
    with open("hydro.log", "a") as of:
        pprint(status_result, stream=of)

