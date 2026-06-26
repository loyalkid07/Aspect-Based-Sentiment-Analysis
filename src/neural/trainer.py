"""Training and evaluation workflow for the Attention Bi-LSTM model."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader

from src.models.attention_bilstm import AspectAttentionBiLSTM
from src.neural.dataset import ABSADataset, load_absa_csv, split_rows
from src.neural.preprocessing import ABSAPreprocessor


@dataclass
class TrainingConfig:
    dataset_path: str = "data/absa_samples.csv"
    artifact_dir: str = "artifacts/attention_bilstm"
    max_length: int = 48
    context_window: int = 4
    embedding_dim: int = 64
    hidden_dim: int = 64
    aspect_embedding_dim: int = 8
    dropout: float = 0.2
    batch_size: int = 8
    epochs: int = 25
    learning_rate: float = 0.003
    seed: int = 42
    refit_on_full_dataset: bool = False


def train_attention_bilstm(config: TrainingConfig) -> dict[str, object]:
    """Train the model and write checkpoint, preprocessing files, and metrics."""
    torch.manual_seed(config.seed)
    rows = load_absa_csv(config.dataset_path)
    train_rows, val_rows, test_rows = split_rows(rows, seed=config.seed)

    preprocessor = ABSAPreprocessor(
        max_length=config.max_length,
        context_window=config.context_window,
    )
    preprocessor.fit(train_rows)

    train_loader = DataLoader(
        ABSADataset(train_rows, preprocessor),
        batch_size=config.batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        ABSADataset(val_rows, preprocessor),
        batch_size=config.batch_size,
    )
    test_loader = DataLoader(
        ABSADataset(test_rows, preprocessor),
        batch_size=config.batch_size,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = _build_model(config, preprocessor).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()

    history = []
    best_state = None
    best_val_accuracy = -1.0

    for epoch in range(1, config.epochs + 1):
        train_metrics = _run_epoch(model, train_loader, criterion, device, optimizer)
        val_metrics = _run_epoch(model, val_loader, criterion, device)
        history.append(
            {
                "epoch": epoch,
                "train": train_metrics,
                "validation": val_metrics,
            }
        )
        if val_metrics["accuracy"] >= best_val_accuracy:
            best_val_accuracy = val_metrics["accuracy"]
            best_state = {key: value.cpu() for key, value in model.state_dict().items()}

    if best_state is not None:
        model.load_state_dict(best_state)
    test_metrics = _run_epoch(model, test_loader, criterion, device)

    checkpoint_model = model
    if config.refit_on_full_dataset:
        checkpoint_model = _train_final_model(rows, preprocessor, config, device)

    artifact_dir = Path(config.artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    preprocessor.save(artifact_dir / "preprocessor.json")
    model_config = {
        "vocab_size": len(preprocessor.vocab),
        "num_labels": len(preprocessor.label_to_id),
        "embedding_dim": config.embedding_dim,
        "hidden_dim": config.hidden_dim,
        "aspect_embedding_dim": config.aspect_embedding_dim,
        "dropout": config.dropout,
            "padding_idx": 0,
        }
    torch.save(
        {
            "model_state_dict": checkpoint_model.state_dict(),
            "model_config": model_config,
            "training_config": asdict(config),
        },
        artifact_dir / "model.pt",
    )

    metrics = {
        "dataset_size": len(rows),
        "split_sizes": {
            "train": len(train_rows),
            "validation": len(val_rows),
            "test": len(test_rows),
        },
        "checkpoint_note": (
            "Holdout metrics were measured before refitting. The saved checkpoint "
            "was refit on the full compact local dataset for demonstration."
            if config.refit_on_full_dataset
            else "Saved checkpoint uses the best validation model."
        ),
        "history": history,
        "test": test_metrics,
    }
    (artifact_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )
    return metrics


def _build_model(
    config: TrainingConfig,
    preprocessor: ABSAPreprocessor,
) -> AspectAttentionBiLSTM:
    return AspectAttentionBiLSTM(
        vocab_size=len(preprocessor.vocab),
        num_labels=len(preprocessor.label_to_id),
        embedding_dim=config.embedding_dim,
        hidden_dim=config.hidden_dim,
        aspect_embedding_dim=config.aspect_embedding_dim,
        dropout=config.dropout,
    )


def _train_final_model(
    rows: list[dict[str, str]],
    preprocessor: ABSAPreprocessor,
    config: TrainingConfig,
    device: torch.device,
) -> AspectAttentionBiLSTM:
    torch.manual_seed(config.seed)
    model = _build_model(config, preprocessor).to(device)
    loader = DataLoader(
        ABSADataset(rows, preprocessor),
        batch_size=config.batch_size,
        shuffle=True,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()
    for _ in range(config.epochs):
        _run_epoch(model, loader, criterion, device, optimizer)
    return model


def _run_epoch(
    model: AspectAttentionBiLSTM,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None = None,
) -> dict[str, float]:
    is_training = optimizer is not None
    model.train(is_training)

    total_loss = 0.0
    total_correct = 0
    total_items = 0
    for batch in loader:
        token_ids = batch["token_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        aspect_mask = batch["aspect_mask"].to(device)
        labels = batch["label"].to(device)

        with torch.set_grad_enabled(is_training):
            logits, _ = model(token_ids, attention_mask, aspect_mask)
            loss = criterion(logits, labels)
            if is_training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        predictions = logits.argmax(dim=1)
        total_loss += loss.item() * labels.size(0)
        total_correct += (predictions == labels).sum().item()
        total_items += labels.size(0)

    if total_items == 0:
        return {"loss": 0.0, "accuracy": 0.0}
    return {
        "loss": total_loss / total_items,
        "accuracy": total_correct / total_items,
    }
