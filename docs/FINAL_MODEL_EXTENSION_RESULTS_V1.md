## Executive summary (read this first)

The final frozen-panel extension completed 48 GLM API and 48 local Llama replies.
GLM reproduces financial denied-credit effects. Llama supplies two unequal-value
credits on one mathematical question but no valid financial reply. These exploratory
arms strengthen observed coverage while preserving negative results and limitations.

| Arm / domain | Attempts | Admitted scalar replies | Released/native credits | Contract/exact credits |
|---|---:|---:|---:|---:|
| GLM / finance | 24 | 24 | 7 | 17 |
| GLM / mathematics | 24 | 23 | 20 | 20 |
| Llama / finance | 24 | 23 | 0 | 0 |
| Llama / mathematics | 24 | 19 | 11 | 9 |

These are paired scoring-policy counts, not a model-ranking table. All attempts
remain in the denominator; seven replies fail the endpoint. No financial valid
reply exists for Llama, so zero denied-valid replies cannot establish robustness.

GLM uses z-ai/glm-4.7-flash through a single Novita BF16 route with fallback disabled.
The 51 requests, including three readiness probes, cost $0.00286891 in recorded
usage. The study cap was $0.50 inside the existing $10 authorization. No request
failed, was retried or carried an unknown charge in this arm. Hosted templates and
weights remain provider-managed; min-p and repetition-penalty defaults differ
from the local configuration.

Llama 3.2 3B uses Q4_K_M weights and native LM Studio templates. The first interface
stage received three HTTP400 responses because Llama exposes no reasoning selector;
no cohort response existed. A disclosed amendment omitted that selector before
cohort collection. Scientific prompts, output cap and scalar parser remained fixed.
The original failed collector, protocol and probes are in the portable bank.

The two mathematical unequal credits are repetitions of the same question. Integer
coefficients and a root 4-sqrt(11) imply the conjugate root and polynomial
p(x)=a(x^2-8x+5), so p(3)/p(4)=10/11. Llama twice expands the constant as 15 and
returns zero; the pinned comparator's integer-part branch nevertheless credits it.
This is an observed local comparison failure, not an estimate of benchmark-wide
prevalence or evidence about historical RecursiveMAS scores.

[Portable replay](../artifacts/final-model-extensions-v1/README.md) checks all 96
scalar decisions and recorded API charges. Full-response extraction is checked
against retained local replies during projection preparation; the public scalar
bank omits original question contexts and explanatory prose. Family, hosting,
checkpoint and quantization differences preclude causal capacity comparisons.
