from .exceptions import BalNLPError
from .schemas import Entity, Token


def word_positions(word_ids: list[int | None], count: int) -> list[list[int]]:
    positions: list[list[int]] = [[] for _ in range(count)]
    for position, word in enumerate(word_ids):
        if word is not None:
            if word < 0 or word >= count:
                raise BalNLPError("INFERENCE_FAILED", "The model returned misaligned tokens.", 500)
            positions[word].append(position)
    if any(not p for p in positions):
        raise BalNLPError("TEXT_TOO_LONG", "A word could not be encoded. Try a shorter sentence.")
    return positions


def merge_predictions(tokens: list[Token], predictions: list[dict], task: str) -> list[Token]:
    allowed = {
        "pos": {"upos"},
        "ner": {"ner"},
        "morph": {"lemma", "feats"},
        "parser": {"head", "deprel"},
    }[task]
    if len(tokens) != len(predictions):
        raise BalNLPError("INFERENCE_FAILED", "The model returned misaligned tokens.", 500)
    merged = []
    for token, prediction in zip(tokens, predictions, strict=True):
        if set(prediction) - allowed:
            raise BalNLPError("INFERENCE_FAILED", "The model returned unsupported fields.", 500)
        merged.append(Token.model_validate(token.model_dump() | prediction))
    return merged


def entities_from_bio(text: str, tokens: list[Token]) -> list[Entity]:
    entities: list[Entity] = []
    current: list[Token] = []
    label = ""

    def flush():
        if current:
            entities.append(
                Entity(
                    text=text[current[0].start : current[-1].end],
                    label=label,
                    start=current[0].start,
                    end=current[-1].end,
                    token_ids=[t.id for t in current],
                )
            )

    for token in tokens:
        tag = token.ner or "O"
        prefix, _, kind = tag.partition("-")
        continues = (
            prefix in {"I", "E"}
            and kind == label
            and current
            and current[-1].sentence_id == token.sentence_id
        )
        if not continues:
            flush()
            current = []
        if prefix in {"B", "I", "E", "S"} and kind:
            label = kind
            current.append(token)
        if prefix in {"E", "S"}:
            flush()
            current = []
    flush()
    return entities
