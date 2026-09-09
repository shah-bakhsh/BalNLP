from .model_base import TokenClassificationWrapper


class BalNER(TokenClassificationWrapper):
    field = "ner"
