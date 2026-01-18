#!/usr/bin/env python
from argparse import ArgumentParser
from atproto import Client
from pprint import pprint
from random import choice
import os
import sys

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def read_file(fn):
    with open(fn) as fi:
        lines = fi.readlines()
    return [line.strip()
            for line in lines
            if not line.startswith("#")]


if __name__ == '__main__':
    argp = ArgumentParser()
    argp.add_argument("--configfile", "-f", default="botconfig.yaml")
    argp.add_argument("config", nargs="?", default="default")
    argp.add_argument("--dry-run", "-d", action='store_true')
    args = argp.parse_args()

    configs = []
    if os.path.exists(args.configfile):
        with open(args.configfile) as cfgfile:
            configs = load(cfgfile, Loader=Loader)
    else:
        print("Specified configuration file not found, terminating",
              file=sys.stderr)
        sys.exit(1)

    if not configs:
        print("No configuration loaded, terminating", file=sys.stderr)
        sys.exit(1)

    if cfg := configs.get(args.config):
        texts = []
        rootdir = os.path.join("posts", cfg.get("path", args.config))
        for fn in os.listdir(rootdir):
            texts.extend(read_file(os.path.join(rootdir, fn)))
        text = choice(texts)
        print("Posting:", text)

        if args.dry_run:
            sys.exit(0)

        client = Client()
        client.login(cfg["username"], cfg["password"])

        status_result = client.send_post(text)
        with open("posts.log", "a") as of:
            pprint(status_result, stream=of)
    else:
        print("Specified configuration not found in file, terminating",
              file=sys.stderr)

