## Executive summary (read this first)

The user's looped-transformer idea is worth pursuing as a **research candidate**, especially for Agenthon Track 2. Applying weight-tied layers to a financial series is already too close to prior art for a strong poster claim. The promising question is whether *extra latent computation has measurable value when dated text changes a calibrated financial forecast*, at a fixed inference budget and without future information. That remains a hypothesis, not an established gap or result.

## Closest papers inspected on 29 September 2026

| Source | Established result | Collision with a simple pitch |
|---|---|---|
| [Yang et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b8402301e7f06bdc97a31bfaa653dc32-Abstract-Conference.html) | Looped transformers can emulate iterative learning algorithms with fewer parameters. | Repeating a block is established. |
| [Dudley and Oymak, 2026, full text](https://arxiv.org/html/2605.11262v2) | Latent feedback and a weight-tied loop are compared on nine time-series datasets, including Exchange; forecasts use MSE. On Exchange, looped gain over the shallow baseline is reported as 1.70% ± 9.17%, and latent-feedback gain as 24.63% ± 2.95%. | A looped financial point forecaster alone is directly anticipated. Their Exchange result is an exchange-rate series, not an Agenthon-style as-of text and probabilistic evaluation. |
| [Seo et al., AIR, 2025, abstract](https://arxiv.org/abs/2512.10229) | Text dynamically routes multivariate time-series inputs; experiments include oil prices and exchange rates. | Text-guided adaptation itself is directly occupied. |
| [Sridhar et al., 2026, ICML workshop](https://arxiv.org/abs/2608.22321) | Audits semantic text sensitivity in multimodal time-series forecasts and releases a perturbation harness. | Text-swap/paraphrase auditing is already a published workshop contribution; a new paper must show an additional causal mechanism or stronger benchmark. |
| [RefineBridge, 2025/2026](https://arxiv.org/abs/2512.21572) | Iterative refinement of time-series foundation-model forecasts is already proposed specifically for finance. | Iterative forecast refinement alone is also occupied. |
| [Popescu et al., 2026](https://arxiv.org/abs/2607.20519) | Adaptive halting and trajectory/readout effects in looped transformers are explicitly analyzed. | A learned stop gate alone is insufficient. |

## Conditional paper hypothesis

**Working question:** Can an as-of-dated evidence token justify more recurrent computation, improving a *probabilistic* financial forecast under the same expected inference budget, rather than merely changing a point prediction?

**Geometric picture:** A forecast is a distribution in prediction space. Each loop is a move in that space. Dated evidence should change both the direction and the distance of the move. We would measure whether successive loops approach the realized outcome's proper-score optimum on truly unseen dates, whether the movement is sensitive to the meaning of valid evidence, and whether the extra compute is worth its cost. The novelty, if any, must be in this evidence × computation interaction and its audited benchmark, not in the recurrent block itself.

**Minimum comparative experiment:** freeze point-in-time numeric/text inputs; compare fixed-depth transformer, parameter-matched looped transformer, compute-matched deeper transformer, latent-feedback baseline from Dudley and Oymak, and a strong probabilistic TS foundation model. Evaluate CRPS, calibration, text-removal/shuffle/meaning-preserving controls, and score gain per additional loop across time-blocked out-of-sample periods. A gate selects extra loops using only as-of information. Include no-text and text-only controls and rigorous source-date checks.

**Kill gates:** If an as-of text corpus is unavailable, if AIR-style text routing already explains the gain, if semantic-text controls reproduce only the existing audit result, if gains vanish against a compute-matched baseline, if a simpler calibration layer matches performance, or if evidence changes predictions without score improvement, do not write it as a new method. Track 2's sealed competition answers cannot become a research artifact; use public-safe research data and do not infer final leaderboard behavior from practice cards.

**Current judgement:** more promising than the observed MarS closed-cycle result, but not yet a confident-acceptance concept. First conduct a full-text comparison of the nearest works, including AIR and inspect the exact Agenthon Track 2 public data contract, then freeze a pilot with genuine dated evidence.
