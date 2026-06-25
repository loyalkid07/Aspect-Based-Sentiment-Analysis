"""Preprocessing utilities for the Attention Bi-LSTM ABSA model."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?|[^\w\s]", re.IGNORECASE)
PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "but",
    "is",
    "of",
    "the",
    "this",
    "to",
    "was",
    "were",
    "while",
}


def tokenize(text: str) -> list[str]:
    """Lowercase and split text into lightweight word/punctuation tokens."""
    return TOKEN_PATTERN.findall(text.lower())


@dataclass
class EncodedExample:
    token_ids: list[int]
    attention_mask: list[int]
    aspect_mask: list[int]
    label_id: int | None
    tokens: list[str]


class ABSAPreprocessor:
    """Builds vocabulary, labels, and tensor-ready features."""

    def __init__(
        self,
        vocab: dict[str, int] | None = None,
        label_to_id: dict[str, int] | None = None,
        max_length: int = 48,
        context_window: int = 4,
    ) -> None:
        self.vocab = vocab or {PAD_TOKEN: 0, UNK_TOKEN: 1}
        self.label_to_id = label_to_id or {
            "negative": 0,
            "neutral": 1,
            "positive": 2,
        }
        self.max_length = max_length
        self.context_window = context_window

    @property
    def id_to_label(self) -> dict[int, str]:
        return {idx: label for label, idx in self.label_to_id.items()}

    def fit(self, rows: Iterable[dict[str, str]]) -> None:
        """Build vocabulary from sentence and aspect text."""
        for row in rows:
            for token in tokenize(row["sentence"]) + tokenize(row["aspect"]):
                if token not in self.vocab:
                    self.vocab[token] = len(self.vocab)

    def encode(
        self,
        sentence: str,
        aspect: str,
        label: str | None = None,
    ) -> EncodedExample:
        tokens = tokenize(sentence)
        aspect_tokens = tokenize(aspect)
        clipped_tokens = tokens[: self.max_length]
        aspect_mask = self._build_aspect_mask(clipped_tokens, aspect_tokens)
        focus_mask = self._build_focus_mask(clipped_tokens, aspect_mask)

        token_ids = [self.vocab.get(token, self.vocab[UNK_TOKEN]) for token in clipped_tokens]
        attention_mask = focus_mask if any(focus_mask) else [1] * len(token_ids)
        pad_count = self.max_length - len(token_ids)
        if pad_count > 0:
            token_ids.extend([self.vocab[PAD_TOKEN]] * pad_count)
            attention_mask.extend([0] * pad_count)
            aspect_mask.extend([0] * pad_count)

        label_id = None if label is None else self.label_to_id[label.lower()]
        return EncodedExample(
            token_ids=token_ids,
            attention_mask=attention_mask,
            aspect_mask=aspect_mask,
            label_id=label_id,
            tokens=clipped_tokens,
        )

    def save(self, path: str | Path) -> None:
        payload = {
            "vocab": self.vocab,
            "label_to_id": self.label_to_id,
            "max_length": self.max_length,
            "context_window": self.context_window,
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ABSAPreprocessor":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            vocab=payload["vocab"],
            label_to_id=payload["label_to_id"],
            max_length=payload["max_length"],
            context_window=payload.get("context_window", 4),
        )

    def _build_aspect_mask(
        self,
        tokens: list[str],
        aspect_tokens: list[str],
    ) -> list[int]:
        mask = [0] * len(tokens)
        if not tokens or not aspect_tokens:
            return mask

        span_start = self._find_subsequence(tokens, aspect_tokens)
        if span_start is not None:
            for index in range(span_start, span_start + len(aspect_tokens)):
                mask[index] = 1
            return mask

        aspect_terms = set(aspect_tokens)
        return [1 if token in aspect_terms else 0 for token in tokens]

    def _build_focus_mask(self, tokens: list[str], aspect_mask: list[int]) -> list[int]:
        """Limit attention to a context window around the requested aspect."""
        aspect_indexes = [index for index, value in enumerate(aspect_mask) if value == 1]
        if not aspect_indexes:
            return [1 if self._is_content_token(token) else 0 for token in tokens]
        start = max(0, min(aspect_indexes) - self.context_window)
        end = min(len(aspect_mask), max(aspect_indexes) + self.context_window + 1)
        focus_mask = []
        for index, token in enumerate(tokens):
            in_window = start <= index < end
            is_aspect = aspect_mask[index] == 1
            focus_mask.append(1 if in_window and (is_aspect or self._is_content_token(token)) else 0)
        return focus_mask

    @staticmethod
    def _is_content_token(token: str) -> bool:
        return any(char.isalnum() for char in token) and token not in STOPWORDS

    @staticmethod
    def _find_subsequence(tokens: list[str], target: list[str]) -> int | None:
        for start in range(0, len(tokens) - len(target) + 1):
            if tokens[start : start + len(target)] == target:
                return start
        return None
