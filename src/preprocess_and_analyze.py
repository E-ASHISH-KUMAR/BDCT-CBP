#!/usr/bin/env python3
"""Dependency-free sentiment analysis pipeline."""
import csv, re, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "social_posts.csv"
OUT = ROOT / "outputs"
POSITIVE = {
    "amazing","easy","love","helpful","excellent","great","beautiful","quickly",
    "fantastic","fast","enjoyed","brilliant","good","recommend","happy","clear",
    "useful","solved","quality","best","wonderful","awesome","perfect"
}
NEGATIVE = {
    "crashing","terrible","disappointed","confusing","poorly","slow","unhelpful",
    "hate","ugly","waste","low","failed","awful","bad","delayed","frustrating",
    "poor","worst","broken","annoying","useless"
}
NEGATORS = {"not","no","never","isn't","wasn't","don't","didn't","wouldn't","cannot"}

def clean_text(text):
    text = (text or "").lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+|#(\w+)", r"\1", text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def predict(text):
    tokens = clean_text(text).split()
    pos = neg = 0
    negate_next = False
    for token in tokens:
        if token in NEGATORS:
            negate_next = True
            continue
        if token in POSITIVE:
            if negate_next: neg += 1
            else: pos += 1
            negate_next = False
        elif token in NEGATIVE:
            if negate_next: pos += 1
            else: neg += 1
            negate_next = False
        else:
            # Keep negation active only for the next meaningful token in this simple demo.
            continue
    score = pos - neg
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return sentiment, score, pos, neg

def main():
    OUT.mkdir(exist_ok=True)
    with INPUT.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"post_id","post_date","platform","text","label"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Input must contain columns: {sorted(required)}")
        posts = []
        for row in reader:
            if not row["post_id"].strip() or not row["text"].strip():
                continue
            sentiment, score, pos, neg = predict(row["text"])
            posts.append({
                "post_id": row["post_id"].strip(),
                "post_date": row["post_date"].strip(),
                "platform": row["platform"].strip() or "Unknown",
                "text": row["text"].strip(),
                "clean_text": clean_text(row["text"]),
                "label": row["label"].strip().lower(),
                "entity": row.get("entity", "").strip() or "Unknown",
                "sentiment": sentiment, "score": score,
                "positive_terms": pos, "negative_terms": neg
            })
    counts = Counter(p["sentiment"] for p in posts)
    by_platform = defaultdict(Counter)
    by_entity = defaultdict(Counter)
    for p in posts:
        by_platform[p["platform"]][p["sentiment"]] += 1
        by_entity[p["entity"]][p["sentiment"]] += 1
    total = len(posts)
    summary = {
        "total_posts": total,
        "sentiment_counts": {s: counts.get(s,0) for s in ["positive","neutral","negative"]},
        "sentiment_percentages": {s: round(100*counts.get(s,0)/total,2) if total else 0 for s in ["positive","neutral","negative"]},
        "platforms": [{"platform": k, **{s: by_platform[k].get(s,0) for s in ["positive","neutral","negative"]},
                       "total": sum(by_platform[k].values())} for k in sorted(by_platform)],
        "entities": [{"entity": k, **{s: by_entity[k].get(s,0) for s in ["positive","neutral","negative"]},
                      "total": sum(by_entity[k].values())} for k in sorted(by_entity)],
        "evaluation": {},
        "method": "rule-based lexicon baseline; Kaggle Twitter Entity Sentiment Analysis dataset"
    }
    labelled = [p for p in posts if p["label"] in {"positive","negative","neutral"}]
    if labelled:
        correct = sum(p["label"] == p["sentiment"] for p in labelled)
        summary["evaluation"] = {
            "labelled_posts": len(labelled),
            "matches": correct,
            "accuracy_percent": round(100*correct/len(labelled),2),
            "note": "Agreement with dataset labels; the rule-based lexicon is a baseline, not a benchmark model."
        }
    with (OUT/"cleaned_posts.csv").open("w",newline="",encoding="utf-8") as f:
        fields = list(posts[0].keys()) if posts else ["post_id","post_date","platform","text","clean_text","label","entity","sentiment","score","positive_terms","negative_terms"]
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(posts)
    with (OUT/"summary.json").open("w",encoding="utf-8") as f: json.dump(summary,f,indent=2)
    with (OUT/"sentiment_counts.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["sentiment","count","percentage"])
        for s in ["positive","neutral","negative"]: w.writerow([s,counts.get(s,0),summary["sentiment_percentages"][s]])
    with (OUT/"platform_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["platform","positive","neutral","negative","total"])
        for p in summary["platforms"]: w.writerow([p["platform"],p["positive"],p["neutral"],p["negative"],p["total"]])
    with (OUT/"entity_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["entity","positive","neutral","negative","total"])
        for entity in summary["entities"]:
            w.writerow([entity["entity"],entity["positive"],entity["neutral"],entity["negative"],entity["total"]])
    print(json.dumps(summary, indent=2))
    print(f"\\nWrote outputs to: {OUT}")

if __name__ == "__main__": main()
