## Executive summary (read this first)

The official MarS 2M checkpoint, configuration/licenses, shared validation archive
and source archive are now cached locally at pinned revisions. Large checkpoint
and validation-file SHA-256 values match the publisher's HF LFS metadata. Tensor
headers were read successfully. No model inference, market rollout or external
cycle audit was performed. This is artifact readiness, not simulator readiness.

## Pinned artifacts

Local ignored cache: `data/external-baselines/mars-2m-pinned-v1/`.
Reusable staging command:

```sh
.venv/bin/python scripts/stage_mars_baseline.py \
  --output-dir data/external-baselines/mars-2m-pinned-v1
```

The command requires a new directory and retains hashes, URLs and exact revisions.
It downloads files but does not execute or extract the official source archive.

- Source revision: `f04dd87a4d56342a6a2fc271cdb158fbacd83674`.
- Model revision: `b8f8c818c2a270844961b975f311457628bf2972`.
- Shared asset revision: `de761abefc1e3c0a8106a03b4fed6fc73cf702d3`.
- Safetensors payload: 10,101,496 bytes, publisher checksum verified.
- Validation archive: 59,980,913 bytes, publisher checksum verified.
- Checkpoint header inspection: 28 tensors, 2,524,624 parameter entries.
- Actual released configuration: 16-dimensional embeddings, one layer, two heads,
  1,024 past orders and discrete price/volume/interval bins.

## Source-level interface and remaining work

The original `OrderModel` uses a Llama causal model plus its own order tokenizer.
The checkpoint is a full order-generation model, not our synthetic linear response
predictor. Its features contain 15 order/state values per historical order.
The validation archive is zstd-compressed pickle according to the official helper;
it has not been unpickled or examined as reset-state data. Its existence does not
establish supported interactive starts or counterfactual pairing.

The official setup pins torch 2.6.0, transformers 4.50.0 and Ray Serve 2.44.0,
plus other dependencies. Our local research environment differs and Ray is not
installed. The README recommends Linux/CUDA Docker and says direct installation
is unsupported. No CPU compatibility claim follows from inspecting checkpoint
headers. Establish a separate pinned runtime before market rollout claims.

Required next artifacts: supported reset-state provenance, model sampling control,
actual exchange fill/cash ledger, terminal liquidation protocol, failed-close
reporting, one-direction impact/decay fidelity comparison and finite cycle bank.
Keep external diagnostics distinct from known-reference causal attribution.

Primary sources:
[official pinned repository](https://github.com/microsoft/MarS/tree/f04dd87a4d56342a6a2fc271cdb158fbacd83674),
[released model](https://huggingface.co/Don-Don/mars-order-2m),
[shared data assets](https://huggingface.co/datasets/Don-Don/mars-order-assets).
