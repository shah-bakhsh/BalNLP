"""BalMorph v2, verbatim model operations from author notebook cell 42."""

from torch import nn


class BalMorphModel(nn.Module):
    def __init__(self, encoder, hidden_size, n_rules, attr_class_counts, dropout=0.1):
        super().__init__()
        self.encoder = encoder
        self.dropout = nn.Dropout(dropout)
        self.lemma_rule_head = nn.Linear(hidden_size, n_rules)
        self.attr_heads = nn.ModuleDict(
            {a: nn.Linear(hidden_size, c) for a, c in attr_class_counts.items()}
        )

    def forward(self, input_ids, attention_mask, pooling="mean"):
        out = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        hidden = out.last_hidden_state
        mask = attention_mask.unsqueeze(-1).float()
        if pooling == "mean":
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-6)
        else:
            pooled = hidden[:, 1, :] if hidden.size(1) > 1 else hidden[:, 0, :]
        pooled = self.dropout(pooled)
        return self.lemma_rule_head(pooled), {a: h(pooled) for a, h in self.attr_heads.items()}
