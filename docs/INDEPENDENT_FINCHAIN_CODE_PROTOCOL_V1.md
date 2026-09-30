## Executive summary (read this first)

This extension checks current template code from an independently authored
financial benchmark producer. It is a source-controlled comparison bank, not a
third recovered historical dataset, expert review or FinChain performance
reproduction. No new model call or paid computation is needed.

Pin FinChain code at `9bd2942b85d992844b77094a8b822aa16832703c` before generation.
The author code returns original question/solution strings. Select these functions
by mathematical task correspondence and inspect their source before generation:

- One-period binomial call: `template_op_medium1`.
- Basic WACC: `template_easy_wacc`.
- Annual compound interest: `template_ci_simple_calculation`.

Generate every seed 0 through 99 separately for each function using the declared
Python `random.Random` runtime. There is no mismatch-conditioned selection,
retry, replacement or stopping gate. Call only inspected function definitions and
literal entity pools; do not execute upstream main scripts or foreign imports.
Preserve and hash original native questions/solutions and every attempt.

Extract the native last-line amount/rate by a declared family-specific grammar.
Unsupported instances remain nondecisions; do not recover another solution number.
Derive exact visible-input reference values with Fraction arithmetic independently
of generator outputs. For calls, check risk-neutral valuation against portfolio
replication and no-arbitrage bounds. For WACC, compare direct weighted financing
cost with an equivalent cash-cost identity. For interest, compare repeated annual
accumulation with the closed form, then subtract principal.

Primary numerical compatibility is within half of one hundredth currency unit or
percentage point of the exact visible-input calculation. Separately evaluate the
source's explicit intermediate rounding: call state prices rounded to cents,
WACC weights to four decimals, compound amount to cents before subtracting
principal. At exact rounding ties preserve both nearest alternatives. These are
interpretation-specific endpoint checks, not broad declarations of bad labels.

Negative controls replace the requested quantity with financing debt, omit the
WACC tax adjustment, or use compound amount instead of compound interest. These
are authored diagnostics. Any coincident call/debt value is a nondiagnostic
numeric collision, not evidence that a call solution computes debt. Report all
controls, identities and family denominators, including supported alternatives.

Freeze this protocol, implementation, source fragments and runtime before any
instance generation. Two authorship pipelines do not prove causal independence
or lack of shared formula sources. The code lineage is explicit; its relationship
to historical paper-instance bytes is unproven. No full reasoning-trace validity,
expert adjudication, population prevalence or training effect is asserted.
