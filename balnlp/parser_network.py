"""BalParser v2: exact architecture supplied by its author on 2026-09-07."""

import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, in_dim, out_dim, dropout):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_dim, out_dim), nn.ReLU(), nn.Dropout(dropout))

    def forward(self, x):
        return self.net(x)


class BiaffineScorer(nn.Module):
    def __init__(self, dep_dim, head_dim, num_labels=1, bias_dep=True, bias_head=True):
        super().__init__()
        self.num_labels, self.bias_dep, self.bias_head = num_labels, bias_dep, bias_head
        self.weight = nn.Parameter(
            torch.zeros(num_labels, head_dim + int(bias_head), dep_dim + int(bias_dep))
        )
        nn.init.xavier_uniform_(self.weight)

    def forward(self, dep, head):
        if self.bias_dep:
            dep = torch.cat([dep, torch.ones_like(dep[..., :1])], dim=-1)
        if self.bias_head:
            head = torch.cat([head, torch.ones_like(head[..., :1])], dim=-1)
        scores = torch.einsum("bhd,lde,bne->blhn", head, self.weight, dep)
        return scores.squeeze(1) if self.num_labels == 1 else scores


class BiaffineParser(nn.Module):
    def __init__(self, encoder, hidden_size, num_deprel, arc_dim=768, rel_dim=256, dropout=0.2):
        super().__init__()
        self.encoder = encoder
        self.root_embedding = nn.Parameter(torch.zeros(hidden_size))
        nn.init.normal_(self.root_embedding, std=0.02)
        self.dep_arc_mlp = MLP(hidden_size, arc_dim, dropout)
        self.head_arc_mlp = MLP(hidden_size, arc_dim, dropout)
        self.dep_rel_mlp = MLP(hidden_size, rel_dim, dropout)
        self.head_rel_mlp = MLP(hidden_size, rel_dim, dropout)
        self.arc_scorer = BiaffineScorer(arc_dim, arc_dim, 1, True, False)
        self.rel_scorer = BiaffineScorer(rel_dim, rel_dim, num_deprel, True, True)

    def forward(self, input_ids, attention_mask, word_to_subword, n_words, pooling="mean"):
        hidden = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        reps = torch.zeros(
            input_ids.size(0),
            max(n_words) + 1,
            hidden.size(-1),
            device=hidden.device,
            dtype=hidden.dtype,
        )
        for b in range(input_ids.size(0)):
            reps[b, 0] = self.root_embedding
            for word, positions in enumerate(word_to_subword[b]):
                reps[b, word + 1] = (
                    hidden[b, positions].mean(0) if pooling == "mean" else hidden[b, positions[0]]
                )
        return (
            self.arc_scorer(self.dep_arc_mlp(reps), self.head_arc_mlp(reps)),
            self.rel_scorer(self.dep_rel_mlp(reps), self.head_rel_mlp(reps)),
        )
