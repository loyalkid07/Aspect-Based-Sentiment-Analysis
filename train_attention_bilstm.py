"""Train the reconstructed Attention Bi-LSTM ABSA model."""

from __future__ import annotations

import argparse
import json

from src.neural.trainer import TrainingConfig, train_attention_bilstm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Attention Bi-LSTM ABSA model")
    parser.add_argument("--dataset", default="data/absa_samples.csv")
    parser.add_argument("--artifact-dir", default="artifacts/attention_bilstm")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=48)
    parser.add_argument("--context-window", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = TrainingConfig(
        dataset_path=args.dataset,
        artifact_dir=args.artifact_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        max_length=args.max_length,
        context_window=args.context_window,
    )
    metrics = train_attention_bilstm(config)
    print(json.dumps({"test": metrics["test"], "split_sizes": metrics["split_sizes"]}, indent=2))
    print(f"Saved artifacts to {args.artifact_dir}")


if __name__ == "__main__":
    main()
