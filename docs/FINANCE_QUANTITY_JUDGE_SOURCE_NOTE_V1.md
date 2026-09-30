## Executive summary (read this first)

A fixed label-free LLM judge is an established comparison baseline. It is useful
for measuring disagreement with numerical scoring, but its output cannot serve
as independent financial truth, especially when actor and judge share a model.
The transfer study preserves this limitation and uses separately locked,
question-only AI references rather than letting the judge define its own target.

## Primary source inspected

Lianmin Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*,
NeurIPS 2023 Datasets and Benchmarks.

- [Official proceedings record](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).
- [Official full paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf).

The abstract and Sections 3.3–3.4 were inspected on September 30, 2026. The paper
examines position, verbosity and self-enhancement effects, and documents incorrect
grading of mathematical/reasoning answers, including susceptibility to candidate
answers. Its self-enhancement experiment explicitly does not establish that the
observed differences identify that bias. Its human-preference agreement is not
evidence of financial-quantity correctness on our corpus.

## Study implication

We compare four observable properties: literal native-label equality, typed
reported-value agreement with AI provisional references, typed executed-expression
agreement, and a fixed label-free quantity-review verdict. These are different
measurement channels; no agreement upgrades any of them into expert adjudication.
The judge sees one candidate, without model/arm identity or reference/score. This
does not remove style effects, shared-model conceptual errors or candidate-induced
reasoning failures. We claim neither a new LLM-judge method nor a replication of
MT-Bench or its human preference evaluation.
