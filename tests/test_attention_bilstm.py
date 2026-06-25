import torch

from src.models.attention_bilstm import AspectAttentionBiLSTM
from src.neural.inference import AttentionBiLSTMPredictor
from src.neural.preprocessing import ABSAPreprocessor


def test_preprocessor_builds_vocab_and_aspect_mask():
    rows = [
        {
            "sentence": "The battery life is excellent but the camera is poor.",
            "aspect": "battery life",
            "label": "positive",
        }
    ]
    preprocessor = ABSAPreprocessor(max_length=12)
    preprocessor.fit(rows)
    encoded = preprocessor.encode(
        rows[0]["sentence"],
        rows[0]["aspect"],
        rows[0]["label"],
    )

    assert preprocessor.vocab["battery"] > 1
    assert encoded.label_id == preprocessor.label_to_id["positive"]
    assert sum(encoded.aspect_mask) == 2
    assert 0 < encoded.attention_mask.count(1) <= len(encoded.tokens)
    assert encoded.attention_mask[encoded.tokens.index("excellent")] == 1
    assert len(encoded.token_ids) == 12


def test_model_forward_shapes_and_attention_sum():
    model = AspectAttentionBiLSTM(vocab_size=20, num_labels=3, embedding_dim=8, hidden_dim=6)
    token_ids = torch.tensor([[2, 3, 4, 0], [5, 6, 0, 0]])
    attention_mask = torch.tensor([[1, 1, 1, 0], [1, 1, 0, 0]])
    aspect_mask = torch.tensor([[0, 1, 0, 0], [1, 0, 0, 0]])

    logits, attention = model(token_ids, attention_mask, aspect_mask)

    assert logits.shape == (2, 3)
    assert attention.shape == (2, 4)
    assert torch.allclose(attention.sum(dim=1), torch.ones(2), atol=1e-6)
    assert attention[0, 3].item() < 1e-6
    assert attention[1, 2].item() < 1e-6


def test_preprocessor_label_mapping_is_stable():
    preprocessor = ABSAPreprocessor(max_length=8)

    assert preprocessor.label_to_id == {
        "negative": 0,
        "neutral": 1,
        "positive": 2,
    }
    assert preprocessor.id_to_label[0] == "negative"


def test_predictor_returns_sentiment_probabilities_and_attention(tmp_path):
    rows = [
        {
            "sentence": "The battery life is excellent.",
            "aspect": "battery life",
            "label": "positive",
        }
    ]
    preprocessor = ABSAPreprocessor(max_length=10)
    preprocessor.fit(rows)
    preprocessor.save(tmp_path / "preprocessor.json")

    model_config = {
        "vocab_size": len(preprocessor.vocab),
        "num_labels": len(preprocessor.label_to_id),
        "embedding_dim": 8,
        "hidden_dim": 6,
        "aspect_embedding_dim": 4,
        "dropout": 0.0,
        "padding_idx": 0,
    }
    model = AspectAttentionBiLSTM(**model_config)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "model_config": model_config,
            "training_config": {},
        },
        tmp_path / "model.pt",
    )

    predictor = AttentionBiLSTMPredictor(tmp_path)
    result = predictor.predict("The battery life is excellent.", "battery life")

    assert result["sentiment_label"] in {"negative", "neutral", "positive"}
    assert 0.0 <= result["confidence"] <= 1.0
    assert set(result["class_probabilities"]) == {"negative", "neutral", "positive"}
    assert result["attention_weights"]
    assert {"token", "weight"} <= set(result["attention_weights"][0])
