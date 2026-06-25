"""Run inference with a saved Attention Bi-LSTM ABSA model."""

from __future__ import annotations

import argparse
import json

from src.neural.inference import AttentionBiLSTMPredictor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict aspect sentiment")
    parser.add_argument("--artifact-dir", default="artifacts/attention_bilstm")
    parser.add_argument("--sentence", required=True)
    parser.add_argument("--aspect", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictor = AttentionBiLSTMPredictor(args.artifact_dir)
    result = predictor.predict(args.sentence, args.aspect)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
