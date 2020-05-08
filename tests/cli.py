#!/usr/bin/env python

import requests


def main():
    # resp = requests.get('http://localhost:8000/video/feed/')
    url = 'http://localhost:8000/video/feed/'
    # r = requests.get(tarball_url, stream=True)
    with requests.get(url, stream=True) as r:
        for line in r.iter_lines():
            print(line)


if __name__ == '__main__':
    main()
