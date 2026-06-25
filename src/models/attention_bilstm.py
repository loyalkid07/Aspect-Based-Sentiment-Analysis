"""
Aspect-aware Attention Bi-LSTM model for ABSA.

The model encodes the full sentence with a bidirectional LSTM, builds an
aspect-conditioned query from the encoded aspect tokens, and attends over the
sentence tokens before classifying sentiment.
"""

from __future__ import annotations

import torch
from torch import nn


class AspectAttentionBiLSTM(nn.Module):
    """Bi-LSTM sentiment classifier with aspect-conditioned attention."""

    def __init__(
        self,
        vocab_size: int,
        num_labels: int,
        embedding_dim: int = 64,
        hidden_dim: int = 64,
        aspect_embedding_dim: int = 8,
        dropout: float = 0.2,
        padding_idx: int = 0,
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
        self.aspect_embedding = nn.Embedding(2, aspect_embedding_dim)
        lstm_input_dim = embedding_dim + aspect_embedding_dim
        self.encoder = nn.LSTM(
            input_size=lstm_input_dim,
            hidden_size=hidden_dim,
            batch_first=True,
            bidirectional=True,
        )
        encoded_dim = hidden_dim * 2
        self.aspect_projection = nn.Linear(encoded_dim, encoded_dim)
        self.token_projection = nn.Linear(encoded_dim, encoded_dim)
        self.attention_vector = nn.Linear(encoded_dim, 1, bias=False)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(encoded_dim, num_labels)

    def forward(
        self,
        token_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        aspect_mask: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Return class logits and token attention weights.

        Args:
            token_ids: Tensor shaped ``[batch, seq_len]``.
            attention_mask: 1 for real tokens and 0 for padding.
            aspect_mask: 1 for tokens that belong to the requested aspect.
        """
        token_embeddings = self.embedding(token_ids)
        aspect_features = self.aspect_embedding(aspect_mask.long().clamp(0, 1))
        encoded_input = torch.cat([token_embeddings, aspect_features], dim=-1)
        encoded_states, _ = self.encoder(encoded_input)

        mask = attention_mask.float()
        aspect_weights = aspect_mask.float() * mask
        aspect_lengths = aspect_weights.sum(dim=1, keepdim=True).clamp_min(1.0)
        aspect_context = (encoded_states * aspect_weights.unsqueeze(-1)).sum(dim=1)
        aspect_context = aspect_context / aspect_lengths

        query = self.aspect_projection(aspect_context).unsqueeze(1)
        token_scores = self.attention_vector(
            torch.tanh(self.token_projection(encoded_states) + query)
        ).squeeze(-1)
        token_scores = token_scores.masked_fill(mask == 0, -1e9)
        attention_weights = torch.softmax(token_scores, dim=1)

        context = torch.bmm(attention_weights.unsqueeze(1), encoded_states).squeeze(1)
        logits = self.classifier(self.dropout(context))
        return logits, attention_weights
