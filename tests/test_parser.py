import itertools

import numpy as np
import pytest
import torch

from balnlp.exceptions import BalNLPError
from balnlp.parser import decode_single_root, validate_heads
from balnlp.parser_network import MLP, BiaffineScorer
from balnlp.tokenizer import tokenize_balochi


def valid(heads):
    if heads.count(0) != 1:
        return False
    for dep in range(1, len(heads) + 1):
        seen, node = set(), dep
        while node:
            if node in seen:
                return False
            seen.add(node)
            node = heads[node - 1]
    return True


def test_mst_matches_exhaustive_objective():
    rng = np.random.default_rng(8)
    for _ in range(8):
        scores = rng.normal(size=(5, 5))
        heads = decode_single_root(scores)
        candidates = [list(h) for h in itertools.product(range(5), repeat=4) if valid(list(h))]
        expected = max(
            sum(scores[h, d + 1] for d, h in enumerate(candidate)) for candidate in candidates
        )
        assert valid(heads)
        assert sum(scores[h, d + 1] for d, h in enumerate(heads)) == pytest.approx(expected)


def test_biaffine_axis_and_bias_match_author_definition():
    scorer = BiaffineScorer(2, 3, 4, True, False)
    dep, head = torch.randn(1, 5, 2), torch.randn(1, 5, 3)
    output = scorer(dep, head)
    for label, h, d in [(0, 1, 2), (3, 4, 1)]:
        expected = head[0, h] @ scorer.weight[label] @ torch.cat([dep[0, d], torch.ones(1)])
        assert output[0, label, h, d].item() == pytest.approx(expected.item(), abs=1e-6)
    assert isinstance(MLP(2, 3, 0.2).net[1], torch.nn.ReLU)


def test_tree_validation_rejects_cycle():
    tokens = tokenize_balochi("بلوچی متن متن")
    for token, head in zip(tokens, [0, 3, 2]):
        token.head, token.deprel = head, "root" if head == 0 else "dep"
    with pytest.raises(BalNLPError, match="cyclic"):
        validate_heads(tokens)
