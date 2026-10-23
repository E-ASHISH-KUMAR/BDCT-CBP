#!/usr/bin/env python3
# Hadoop Streaming mapper: input CSV rows; output sentiment<TAB>1.
# For a production CSV with commas/quotes, preprocess to TSV first.
import csv, sys, re
POS={"amazing","easy","love","helpful","excellent","great","beautiful","fantastic","fast","brilliant","good","happy","clear","useful"}
NEG={"crashing","terrible","disappointed","confusing","slow","unhelpful","hate","ugly","waste","awful","bad","delayed","frustrating","poor","worst"}
for line in sys.stdin:
    try:
        row=next(csv.reader([line]))
        if len(row)<4 or row[0]=="post_id": continue
        text=re.sub(r"[^a-z\s]"," ",row[3].lower()).split()
        score=sum(1 for x in text if x in POS)-sum(1 for x in text if x in NEG)
        label="positive" if score>0 else "negative" if score<0 else "neutral"
        print(f"{label}\t1")
    except Exception:
        continue
