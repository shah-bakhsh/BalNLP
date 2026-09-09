from .model_base import TokenClassificationWrapper


class BalPOS(TokenClassificationWrapper):
    field = "upos"
