"""Optional operator-only warmup, e.g. python -m scripts.warmup --tasks pos ner."""

import argparse

from balnlp import BalNLP


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs="+", choices=["pos", "ner", "parser"], default=["pos"])
    args = parser.parse_args()
    nlp = BalNLP.from_pretrained()
    try:
        for task in args.tasks:
            result = nlp.analyze("بلوچی متن", [task])
            print(f"{task}: completed in {result.meta.total_ms:.0f} ms")
    finally:
        nlp.close()


if __name__ == "__main__":
    main()
