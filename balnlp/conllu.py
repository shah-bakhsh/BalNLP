from itertools import groupby

from .schemas import AnalysisResult


def to_conllu(result: AnalysisResult) -> str:
    lines = []
    for sid, iterator in groupby(result.tokens, key=lambda t: t.sentence_id):
        tokens = list(iterator)
        local_ids = {t.id: i + 1 for i, t in enumerate(tokens)}
        text = result.text[tokens[0].start : tokens[-1].end].replace("\n", " ").replace("\r", " ")
        lines += [f"# sent_id = {sid}", f"# text = {text}"]
        for i, token in enumerate(tokens):
            feats = "|".join(f"{k}={v}" for k, v in sorted((token.feats or {}).items())) or "_"
            head = (
                "_" if token.head is None else str(0 if token.head == 0 else local_ids[token.head])
            )
            misc = (
                "SpaceAfter=No" if i + 1 < len(tokens) and token.end == tokens[i + 1].start else "_"
            )
            fields = [
                str(i + 1),
                token.form,
                token.lemma or "_",
                token.upos or "_",
                "_",
                feats,
                head,
                token.deprel or "_",
                "_",
                misc,
            ]
            lines.append("\t".join(fields))
        lines.append("")
    return "\n".join(lines) + "\n"
