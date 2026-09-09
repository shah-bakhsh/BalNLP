from itertools import groupby

from .config import Settings
from .exceptions import BalNLPError
from .model_base import BaseWrapper, ModelSource


def validate_heads(tokens):
    for _, sentence in groupby(tokens, lambda t: t.sentence_id):
        words = list(sentence)
        ids = {t.id for t in words}
        heads = {t.id: t.head for t in words}
        if sum(t.head == 0 for t in words) != 1:
            raise BalNLPError(
                "INFERENCE_FAILED", "The parser did not produce a single-root tree.", 500
            )
        for token in words:
            if (
                token.head not in ids | {0}
                or token.head == token.id
                or not token.deprel
                or (token.head == 0) != (token.deprel == "root")
            ):
                raise BalNLPError(
                    "INFERENCE_FAILED", "The parser returned an invalid dependency.", 500
                )
            seen, node = set(), token.id
            while node:
                if node in seen:
                    raise BalNLPError("INFERENCE_FAILED", "The parser returned a cyclic tree.", 500)
                seen.add(node)
                node = heads[node]


def decode_single_root(scores):
    """Exact non-projective single-root maximum spanning arborescence.

    scores[head, dependent], with artificial root index 0. Evaluate each possible
    root child, then select the highest-scoring tree. Input is bounded upstream.
    """
    import networkx as nx
    import numpy as np

    scores = np.asarray(scores, dtype=float)
    n = len(scores)
    if scores.shape != (n, n) or n < 2 or np.isnan(scores).any():
        raise BalNLPError("INFERENCE_FAILED", "Invalid dependency scores.", 500)
    best, best_score = None, float("-inf")
    # If the unrestricted optimum already has one root, it is also the exact
    # constrained optimum. Avoid solving N additional arborescences in that case.
    graph = nx.DiGraph()
    graph.add_nodes_from(range(n))
    for dep in range(1, n):
        for head in range(n):
            if dep != head and np.isfinite(scores[head, dep]):
                graph.add_edge(head, dep, weight=float(scores[head, dep]))
    try:
        tree = nx.maximum_spanning_arborescence(graph)
        if tree.out_degree(0) == 1:
            parents = {dep: head for head, dep in tree.edges}
            return [parents[dep] for dep in range(1, n)]
    except nx.NetworkXException:
        # The constrained loop below provides the same safe public error.
        tree = None
    for root_child in range(1, n):
        graph = nx.DiGraph()
        graph.add_nodes_from(range(n))
        for dep in range(1, n):
            for head in range(n):
                if dep == head or (head == 0) != (dep == root_child):
                    continue
                if np.isfinite(scores[head, dep]):
                    graph.add_edge(head, dep, weight=float(scores[head, dep]))
        try:
            tree = nx.maximum_spanning_arborescence(graph)
        except nx.NetworkXException:
            continue
        total = tree.size(weight="weight")
        if total > best_score and tree.in_degree(0) == 0:
            best_score = total
            best = [0] * n
            for head, dep in tree.edges:
                best[dep] = head
    if best is None:
        raise BalNLPError("INFERENCE_FAILED", "No valid dependency tree could be decoded.", 500)
    return best[1:]


class BalParser(BaseWrapper):
    """Exact architecture supplied by the author; strict checkpoint loading."""

    @classmethod
    def from_pretrained(cls, model_id, settings=None, revision=None):
        from pathlib import Path

        import torch
        from transformers import AutoConfig, AutoModel, AutoTokenizer

        from .parser_network import BiaffineParser

        source = ModelSource(model_id, settings or Settings(), revision)
        metadata = source.json("configs/model_config.json")
        config = AutoConfig.from_pretrained(
            source.file("model/encoder/config.json"), trust_remote_code=False
        )
        if metadata.get("pooling") != "mean" or metadata.get("decoder") != "mst-single-root":
            raise BalNLPError(
                "MODEL_LOAD_FAILED",
                "The parser configuration is incompatible with this adapter.",
                503,
            )
        with torch.device("meta"):
            model = BiaffineParser(
                AutoModel.from_config(config, trust_remote_code=False),
                metadata["hidden_size"],
                metadata["num_deprel"],
                metadata["arc_mlp_dim"],
                metadata["rel_mlp_dim"],
                metadata["dropout"],
            )
        # Despite its filename, parser_head.pt contains the complete trained encoder.
        state = torch.load(
            source.file("model/parser_head.pt"), map_location="cpu", weights_only=True, mmap=True
        )
        model.load_state_dict(state, strict=True, assign=True)
        del state
        # XLM-R's deterministic nonpersistent buffers are absent from state_dict.
        # Recreate exactly as in XLMRobertaEmbeddings, without reallocating weights.
        embeddings = model.encoder.embeddings
        embeddings.position_ids = torch.arange(config.max_position_embeddings).expand((1, -1))
        embeddings.token_type_ids = torch.zeros(embeddings.position_ids.size(), dtype=torch.long)
        tokenizer_path = source.file("tokenizer/tokenizer.json")
        source.file("tokenizer/tokenizer_config.json")
        tokenizer = AutoTokenizer.from_pretrained(
            str(Path(tokenizer_path).parent), use_fast=True, trust_remote_code=False
        )
        wrapper = cls(source, model, tokenizer)
        wrapper.labels = {int(k): v for k, v in source.json("data/id2deprel.json").items()}
        if set(wrapper.labels) != set(range(metadata["num_deprel"])):
            raise BalNLPError(
                "MODEL_LOAD_FAILED", "Parser relation labels do not match its head.", 503
            )
        wrapper.max_length = metadata["max_len"]
        return wrapper

    def predict(self, tokens):
        import torch

        predictions = []
        with torch.inference_mode():
            for words, encoded, positions in self.batches(tokens, self.max_length):
                if len(words) > self.source.settings.max_parser_words:
                    raise BalNLPError(
                        "TEXT_TOO_LONG", "Please split long sentences before dependency parsing."
                    )
                arcs, relations = self.model(
                    encoded["input_ids"],
                    encoded["attention_mask"],
                    [positions],
                    [len(words)],
                    pooling="mean",
                )
                heads = decode_single_root(arcs[0].float().cpu().numpy())
                dep = torch.arange(1, len(words) + 1, device=self.device)
                chosen = torch.tensor(heads, device=self.device)
                labels = relations[0, :, chosen, dep].transpose(0, 1).argmax(-1).tolist()
                for head, relation in zip(heads, labels, strict=True):
                    predictions.append(
                        {
                            "head": 0 if head == 0 else words[head - 1].id,
                            "deprel": self.labels[relation],
                        }
                    )
        return predictions
