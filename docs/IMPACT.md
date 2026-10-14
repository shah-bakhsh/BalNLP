# Impact and evidence

Snapshot: 2026-09-21. BalNLP's goal is to make Arabic-script Balochi model experimentation
accessible through a common Python/API/UI contract. It addresses a concrete integration
problem: separate checkpoints need consistent token alignment, loading, error handling,
and export. The project focuses on low-resource language tooling; no claim of being
the first or only Balochi NLP system is made here.

## Implemented capabilities

Source in `balnlp/`, `backend/`, and `frontend/` implements POS, NER, morphology,
dependency parsing, RTL interaction, and JSON/CoNLL-U export. Related model links are
listed in the [README](../README.md#models). BalTokenizer is a separate research project,
not the tokenizer substituted into these checkpoints. See [evaluation](EVALUATION.md)
for the limits of existing evidence.

Potential uses include researcher experiments, student NLP exercises, annotation
review, and developer API integration. These are intended uses, not verified deployments
by external institutions. The owner approved Apache-2.0 for owned application source on 2026-09-22;
this does not change the dated adoption snapshot below.

## Adoption snapshot

| Metric | Observed value | Evidence |
|---|---:|---|
| GitHub stars | 0 | Repository API on 2026-09-21 |
| GitHub forks | 0 | Repository API on 2026-09-21 |
| GitHub releases | 0 | Releases endpoint on 2026-09-21 |

Sources: `https://api.github.com/repos/shah-bakhsh/BalNLP` and
`https://api.github.com/repos/shah-bakhsh/BalNLP/releases`.
Downloads, dependents, external contributor counts, citations, and downstream users
were not established by this audit and are omitted. Absence of verified data is not
a claim of zero. GitHub metrics do not measure linguistic quality or community need.

Future evidence should link actual external contributions, permissioned user reports,
reproducible studies, and registry statistics with observation dates and definitions.
Do not turn prospective beneficiaries into claimed users.
