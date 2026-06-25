"""Inference helper for saved Attention Bi-LSTM artifacts."""

from __future__ import annotations

from pathlib import Path

import torch

from src.models.attention_bilstm import AspectAttentionBiLSTM
from src.neural.preprocessing import ABSAPreprocessor


class AttentionBiLSTMPredictor:
    """Loads trained artifacts and predicts sentiment for sentence/aspect pairs."""

    def __init__(self, artifact_dir: str | Path = "artifacts/attention_bilstm") -> None:
        self.artifact_dir = Path(artifact_dir)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessor = ABSAPreprocessor.load(self.artifact_dir / "preprocessor.json")
        checkpoint = _load_checkpoint(self.artifact_dir / "model.pt", self.device)
        self.model = AspectAttentionBiLSTM(**checkpoint["model_config"]).to(self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    def predict(self, sentence: str, aspect: str) -> dict[str, object]:
        encoded = self.preprocessor.encode(sentence, aspect)
        token_ids = torch.tensor([encoded.token_ids], dtype=torch.long, device=self.device)
        attention_mask = torch.tensor(
            [encoded.attention_mask],
            dtype=torch.long,
            device=self.device,
        )
        aspect_mask = torch.tensor([encoded.aspect_mask], dtype=torch.long, device=self.device)

        with torch.no_grad():
            logits, attention = self.model(token_ids, attention_mask, aspect_mask)
            probabilities = torch.softmax(logits, dim=1).squeeze(0).cpu()
            predicted_id = int(probabilities.argmax().item())

        id_to_label = self.preprocessor.id_to_label
        attention_values = attention.squeeze(0).cpu().tolist()[: len(encoded.tokens)]
        class_probabilities = {
            id_to_label[index]: float(probabilities[index])
            for index in range(len(probabilities))
        }
        return {
            "sentence": sentence,
            "aspect": aspect,
            "sentiment_label": id_to_label[predicted_id],
            "confidence": float(probabilities[predicted_id]),
            "class_probabilities": class_probabilities,
            "attention_weights": [
                {"token": token, "weight": float(weight)}
                for token, weight in zip(encoded.tokens, attention_values)
            ],
        }


def _load_checkpoint(path: Path, device: torch.device) -> dict[str, object]:
    try:
        return torch.load(path, map_location=device, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=device)
