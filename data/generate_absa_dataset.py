"""Generate a deterministic synthetic ABSA dataset for local model training.

The examples are template-based, but each row still has explicit sentence,
aspect, and label fields. This keeps the project self-contained while providing
enough variation for the Attention Bi-LSTM pipeline to train and be reviewed.
"""

from __future__ import annotations

import csv
import itertools
from pathlib import Path


OUTPUT_PATH = Path(__file__).with_name("absa_samples.csv")

POSITIVE_PHRASES = [
    "excellent",
    "reliable",
    "impressive",
    "smooth",
    "comfortable",
    "bright",
    "durable",
    "convenient",
    "responsive",
    "well designed",
]
NEGATIVE_PHRASES = [
    "disappointing",
    "poor",
    "unreliable",
    "slow",
    "uncomfortable",
    "dull",
    "fragile",
    "confusing",
    "noisy",
    "overpriced",
]
NEUTRAL_PHRASES = [
    "average",
    "okay",
    "ordinary",
    "acceptable",
    "standard",
    "moderate",
]

DOMAINS = {
    "phone": ["battery life", "camera quality", "display", "speaker", "price", "performance"],
    "laptop": ["keyboard", "screen", "trackpad", "battery", "build quality", "cooling"],
    "restaurant": ["food", "service", "ambience", "menu", "price", "dessert"],
    "hotel": ["room", "location", "staff", "Wi-Fi", "breakfast", "check-in"],
    "headphones": ["sound quality", "noise cancellation", "comfort", "battery", "microphone", "case"],
    "app": ["interface", "login process", "notifications", "search", "checkout", "support"],
    "movie": ["acting", "story", "music", "visuals", "dialogue", "pacing"],
    "course": ["content", "assignments", "instructor", "examples", "quizzes", "feedback"],
    "car": ["mileage", "seats", "steering", "suspension", "engine", "interior"],
    "watch": ["display", "strap", "battery", "tracking", "sync", "design"],
    "book": ["cover", "paper quality", "story", "characters", "editing", "layout"],
    "shoes": ["sole", "fit", "style", "material", "grip", "cushioning"],
}

SINGLE_TEMPLATES = [
    "The {aspect} of this {domain} is {opinion}.",
    "I found the {aspect} on the {domain} to be {opinion}.",
    "For this {domain}, the {aspect} feels {opinion}.",
    "The {domain}'s {aspect} is {opinion} after daily use.",
]

CONTRAST_TEMPLATES = [
    "The {aspect_a} of this {domain} is {opinion_a}, but the {aspect_b} is {opinion_b}.",
    "I liked the {aspect_a} because it was {opinion_a}, although the {aspect_b} was {opinion_b}.",
    "The {domain} has {opinion_a} {aspect_a}, while the {aspect_b} is {opinion_b}.",
]


def main() -> None:
    rows = []
    for domain, aspects in DOMAINS.items():
        rows.extend(_single_aspect_rows(domain, aspects))
        rows.extend(_contrast_rows(domain, aspects))

    unique_rows = list({(row["sentence"], row["aspect"], row["label"]): row for row in rows}.values())
    unique_rows.sort(key=lambda row: (row["sentence"], row["aspect"], row["label"]))

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["sentence", "aspect", "label"])
        writer.writeheader()
        writer.writerows(unique_rows)

    print(f"Wrote {len(unique_rows)} rows to {OUTPUT_PATH}")


def _single_aspect_rows(domain: str, aspects: list[str]) -> list[dict[str, str]]:
    rows = []
    phrase_groups = [
        ("positive", POSITIVE_PHRASES),
        ("negative", NEGATIVE_PHRASES),
        ("neutral", NEUTRAL_PHRASES),
    ]
    for aspect, template, (label, phrases) in itertools.product(aspects, SINGLE_TEMPLATES, phrase_groups):
        for opinion in phrases:
            rows.append(
                {
                    "sentence": template.format(domain=domain, aspect=aspect, opinion=opinion),
                    "aspect": aspect,
                    "label": label,
                }
            )
    return rows


def _contrast_rows(domain: str, aspects: list[str]) -> list[dict[str, str]]:
    rows = []
    aspect_pairs = list(zip(aspects[::2], aspects[1::2]))
    sentiment_pairs = [
        ("positive", POSITIVE_PHRASES, "negative", NEGATIVE_PHRASES),
        ("negative", NEGATIVE_PHRASES, "positive", POSITIVE_PHRASES),
        ("positive", POSITIVE_PHRASES, "neutral", NEUTRAL_PHRASES),
        ("neutral", NEUTRAL_PHRASES, "negative", NEGATIVE_PHRASES),
    ]
    for aspect_a, aspect_b in aspect_pairs:
        for template in CONTRAST_TEMPLATES:
            for label_a, phrases_a, label_b, phrases_b in sentiment_pairs:
                for opinion_a, opinion_b in zip(phrases_a, phrases_b):
                    sentence = template.format(
                        domain=domain,
                        aspect_a=aspect_a,
                        aspect_b=aspect_b,
                        opinion_a=opinion_a,
                        opinion_b=opinion_b,
                    )
                    rows.append({"sentence": sentence, "aspect": aspect_a, "label": label_a})
                    rows.append({"sentence": sentence, "aspect": aspect_b, "label": label_b})
    return rows


if __name__ == "__main__":
    main()
