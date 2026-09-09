import os

import pytest

from balnlp import BalNLP
from balnlp.parser import validate_heads

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("BALNLP_RUN_INTEGRATION") != "1", reason="Real checkpoint tests are opt-in"
    ),
]


@pytest.mark.parametrize("task", ["pos", "ner", "morph", "parser"])
def test_real_checkpoint(task):
    nlp = BalNLP.from_pretrained()
    try:
        result = nlp.analyze("بلوچی متن", tasks=[task])
        assert result.meta.completed_tasks == [task]
        assert len(result.tokens) == 2
        if task == "pos":
            assert all(
                token.upos and not token.upos.startswith("LABEL_") for token in result.tokens
            )
        if task == "ner":
            assert all(token.ner is not None for token in result.tokens)
        if task == "morph":
            assert all(
                token.lemma is not None and token.feats is not None for token in result.tokens
            )
        if task == "parser":
            validate_heads(result.tokens)
            assert all(token.deprel for token in result.tokens)
        assert all(
            len(line.split("\t")) == 10
            for line in result.conllu.splitlines()
            if line and not line.startswith("#")
        )
    finally:
        nlp.close()
