# Recovered Attention Bi-LSTM ABSA Model

This guide documents the reconstructed neural component of the project. The
existing app still uses the original dependency-parsing and VADER pipeline. The
Attention Bi-LSTM path is separate so the college-era neural work can be
reviewed, trained, and demonstrated without destabilizing the deployed app.

## What It Implements

The neural model treats ABSA as aspect-level sentiment classification. Each
training row contains:

```csv
sentence,aspect,label
"The battery life is excellent, but the camera quality is disappointing.","battery life",positive
"The battery life is excellent, but the camera quality is disappointing.","camera quality",negative
```

The pipeline performs tokenization, vocabulary construction, sequence padding,
label encoding, aspect-span masking, and content-aware aspect-window masking.
The aspect mask lets the model know which tokens represent the target aspect,
while the attention mask keeps the learned attention distribution on meaningful
tokens around that aspect instead of padding, punctuation, or common function
words.

## Architecture

The model in `src/models/attention_bilstm.py` uses:

1. Word embeddings for sentence tokens.
2. A small aspect-position embedding that marks target-aspect tokens.
3. A bidirectional LSTM that reads the full sentence from left-to-right and
   right-to-left.
4. An aspect-conditioned attention layer that builds a query from encoded
   aspect tokens and scores content tokens in the aspect-centered context
   window.
5. A classifier head for `negative`, `neutral`, and `positive`.

This is intentionally more than a placeholder: the attention weights are
computed by the model and returned at inference time for inspection.

## Training

Train the model from the project root:

```bash
python train_attention_bilstm.py
```

The command reads `data/absa_samples.csv`, splits it into train, validation, and
test sets, and writes generated artifacts to:

```text
artifacts/attention_bilstm/
```

The generated files are:

- `model.pt`: PyTorch checkpoint.
- `preprocessor.json`: vocabulary, labels, and max sequence length.
- `metrics.json`: train/validation history and test metrics.

Because the included dataset is compact, the metrics are useful for smoke
testing and demonstration only. They should not be presented as benchmark
results.

## Inference

After training, run:

```bash
python predict_attention_bilstm.py \
  --sentence "The battery life is excellent, but the camera quality is disappointing." \
  --aspect "battery life"
```

The output includes:

- `sentiment_label`
- `confidence`
- `class_probabilities`
- `attention_weights`, one score per visible token

Run the same sentence with `--aspect "camera quality"` to inspect whether the
attention distribution changes for the different target aspect.

## How This Supports The Resume Points

- The Bi-LSTM processes the sentence in both directions, giving each token
  access to left and right context.
- The aspect mask identifies the target aspect, so the classifier is not just
  predicting sentence-level sentiment.
- The attention layer uses the encoded aspect representation to focus on the
  words most relevant to that aspect.
- The training and inference scripts make the work reproducible and reviewable.

## Limitations

This reconstruction uses a small local dataset to avoid external downloads and
to keep the project self-contained. It demonstrates the architecture and
workflow, but stronger accuracy claims would require training and evaluating on
a recognized ABSA benchmark such as SemEval restaurant or laptop reviews.
