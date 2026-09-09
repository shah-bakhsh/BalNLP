"""Measure one real model at a time: python -m scripts.memory_probe --task pos."""

import argparse
import json

from balnlp import BalNLP
from balnlp.memory import memory_diagnostics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["pos", "ner", "parser"], default="pos")
    args = parser.parse_args()
    nlp = BalNLP.from_pretrained(balnlp_memory_mode="balanced")
    report = {"task": args.task, "before": memory_diagnostics(nlp.settings)}
    try:
        nlp.manager.load_model(args.task)
        report["loaded"] = memory_diagnostics(nlp.settings)
        result = nlp.analyze("بلوچی متن", [args.task])
        report["after_inference"] = memory_diagnostics(nlp.settings)
        report["completed_tasks"] = result.meta.completed_tasks
        report["inference_ms"] = result.meta.total_ms
    finally:
        nlp.close()
    report["after_unload"] = memory_diagnostics(nlp.settings)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
