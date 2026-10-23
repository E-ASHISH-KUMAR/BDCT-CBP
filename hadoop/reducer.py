#!/usr/bin/env python3
import sys
current=None; total=0
for line in sys.stdin:
    key, _, value = line.rstrip("\n").partition("\t")
    try: value=int(value)
    except ValueError: continue
    if current is not None and key != current:
        print(f"{current}\t{total}")
        total=0
    current=key; total += value
if current is not None: print(f"{current}\t{total}")
