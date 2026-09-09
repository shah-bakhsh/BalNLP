from types import SimpleNamespace

import pytest
import torch
from torch import nn

from balnlp.morph_adapter import decode_rule
from balnlp.morph_network import BalMorphModel


@pytest.mark.parametrize(
    "word,rule,expected",
    [
        ("abcd", "2::xy", "abxy"),
        ("abc", "0::", "abc"),
        ("abc", "9::x", "x"),
        ("abc", "1::x::y", "abx::y"),
        ("abc", "<UNK_RULE>", None),
    ],
)
def test_notebook_rule_reconstruction(word, rule, expected):
    assert decode_rule(word, rule) == expected


def test_notebook_mean_includes_special_tokens_and_excludes_padding():
    class Encoder(nn.Module):
        def forward(self, input_ids, attention_mask):
            return SimpleNamespace(last_hidden_state=input_ids.float().unsqueeze(-1))

    model = BalMorphModel(Encoder(), 1, 1, {"Case": 1}, dropout=0)
    with torch.no_grad():
        model.lemma_rule_head.weight.fill_(1)
        model.lemma_rule_head.bias.zero_()
        model.attr_heads["Case"].weight.fill_(2)
        model.attr_heads["Case"].bias.zero_()
    rules, attrs = model(torch.tensor([[2, 4, 6, 100]]), torch.tensor([[1, 1, 1, 0]]))
    assert rules.item() == 4
    assert attrs["Case"].item() == 8
