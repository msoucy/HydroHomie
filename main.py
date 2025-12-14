#!/usr/bin/env python
from atproto import Client
from dotenv import load_dotenv
from pprint import pprint
from random import choice
import os


def readFile(fn):
    with open(fn) as fi:
        lines = fi.readlines()
    return [line.strip()
            for line in lines
            if not line.startswith("#")]

if __name__ == '__main__':
    load_dotenv()
    texts = readFile("hydro.txt")
    text = choice(texts)
    print("Posting:", text)

    client = Client()
    client.login(os.environ["BSKY_USERNAME"], os.environ["BSKY_PASSWORD"])

    status_result = client.send_post(text)
    with open("posts.log", "a") as of:
        pprint(status_result, stream=of)

