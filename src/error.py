#!/usr/bin/env python3

def pr(data: str, lines: list | tuple | dict, error=None) -> None:
    print(f"Error while scraping data: {data}")
    for n, li in enumerate(lines):
        print(n, ":", li)
    if error:
        print(repr(error))
    exit(1)
