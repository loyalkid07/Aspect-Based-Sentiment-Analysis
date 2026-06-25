"""Dataset loading and batching for neural ABSA."""

from __future__ import annotations

import csv
import random
from pathlib import Path

import torch
from torch.utils.data import Dataset

from src.neural.preprocessing import ABSAPreprocessor


def load_absa_csv(path: str | Path) -> list[dict[str, str]]:
    """Load rows with sentence, aspect, and label fields."""
    with Path(path).open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    required = {"sentence", "aspect", "label"}
    for row in rows:
        missing = required.difference(row)
        if missing:
            raise ValueError(f"Missing fields in dataset: {sorted(missing)}")
        row["label"] = row["label"].lower()
    return rows


def split_rows(
    rows: list[dict[str, str]],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Deterministically split rows into train, validation, and test sets."""
    shuffled = list(rows)
    random.Random(seed).shuffle(shuffled)
    train_end = int(len(shuffled) * train_ratio)
    val_end = train_end + int(len(shuffled) * val_ratio)
    return shuffled[:train_end], shuffled[train_end:val_end], shuffled[val_end:]


class ABSADataset(Dataset):
    """Torch dataset for sentence/aspect sentiment examples."""

    def __init__(self, rows: list[dict[str, str]], preprocessor: ABSAPreprocessor) -> None:
        self.rows = rows
        self.preprocessor = preprocessor

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        row = self.rows[index]
        encoded = self.preprocessor.encode(row["sentence"], row["aspect"], row["label"])
        return {
            "token_ids": torch.tensor(encoded.token_ids, dtype=torch.long),
            "attention_mask": torch.tensor(encoded.attention_mask, dtype=torch.long),
            "aspect_mask": torch.tensor(encoded.aspect_mask, dtype=torch.long),
            "label": torch.tensor(encoded.label_id, dtype=torch.long),
        }
