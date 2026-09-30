## Executive summary (read this first)

Use NeurIPS main-track standards to organize and audit the paper, while submitting
under Agenthon's actual workshop rules. Main-track formatting does not establish
main-track acceptance or scientific quality. The current source remains the same
open standalone editor file; no separate PDF or replacement document is created.

Checked the [official 2026 main-track handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook),
[CFP and linked template](https://neurips.cc/Conferences/2026/CallForPapers),
[workshop call](https://neurips.cc/Conferences/2026/CallForWorkshops), and
[Agenthon paper call](https://www.agenthon.net/#call-for-papers) on September 30.
The general workshop call concerns organizing workshops, not a universal paper
length or template requirement for every workshop contribution.

## Verified rule comparison

| Requirement | NeurIPS 2026 main track | This Agenthon workshop CFP |
|---|---|---|
| Main-body length | At most nine content pages, including tables and figures; ten camera-ready after acceptance. | Full or short papers, any length. |
| Template | Official current-year LaTeX style; font/margin changes to evade limits forbidden. | Any format, one PDF. |
| PDF organization | Suggested order: body, references, supporting appendices, mandatory paper checklist. | No specific order or checklist is stated. |
| Reference/appendix pages | Do not count toward the nine content pages. | No page-count restriction stated. |
| Identity | Main-track submissions double blind; named public preprints use the preprint option. | Public CFP does not state an anonymous-review rule. Named solo-author paper retained. |
| PDF size | 50MB maximum. | A size limit is not stated in the public CFP; actual form restriction unverified. |
| Scientific expectations | Quality, clarity, significance and originality; justified experiments and reproducibility. | Broad AI/finance scope includes evaluation, verification and benchmarks; no detailed scoring rubric published. |
| Publication | Main-conference proceedings after acceptance. | Non-archival poster presentation, author attendance required. |

The main-track deadline was May 6, 2026. The live workshop deadline is September
30, 23:59 AoE (October 1, 13:59 Berlin). Different routes must not be conflated.
Agenthon's specific CFP governs its contribution format/deadline; a generic
workshop-organizer call does not replace that information.

## Practical target for this draft

A full-paper presentation is the default recommendation: a compact body organized
around the financial quantity defect and fixed-answer grading consequences,
recognizable FinQA/TAT-QA extension, then references and appendices. Nine content
pages is a voluntary editing target for this workshop, not an Agenthon rule.
The optional user preference question distinguishes this from a 4–6-page workshop
body. No page-limit compliance is claimed until the rendered body is measured.

Keep headline definitions, selection/limitations, passing controls and the primary
paired grading result in the body. Move large model-by-family tables, unsuccessful
GEPA details, full exploration graph and implementation diagnostics to appendices.
Do not achieve the target by smaller fonts or narrowed margins.

Use the official current-year template if the standalone native compiler can
support it without requiring external project files. Otherwise retain the
compileable source and report the limitation; a hand-approximated style is not
certified official main-track formatting. Never use an accepted-paper footer or
claim the paper is under NeurIPS review because it uses the template.

## Citation standard

There is no cited minimum bibliography count. Add sources where they substantiate
methods, identify the closest contribution collision, justify a baseline or
document a resource. References should connect to claims in the text, rather than
only appearing in a longer bibliography. Verify author/title/venue/year/URL
against primary publisher/author records and distinguish preprint versions from
publication records. Record inaccessible full text without inventing its content.

The prior bibliography had 23 entries. Four verified additions bring it to 27: CheckList
(behavioral NLP tests), PAL (interpreter baseline), Datasheets (dataset context),
and Pineau et al.'s NeurIPS reproducibility-program report. They address real gaps
in the current positioning; adding organizer names alone would not.
The completed local checkpoint replication adds Google's official Gemma 4 model
card as a resource citation, bringing the current bibliography to 28. A model
card is not presented as another peer-reviewed research result.

## Implemented format checks

The official template ZIP was obtained through the current CFP link:
`https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip`.
ZIP SHA256: `82473931e3ef710fcd3f4a8cd4119b9de32e56825f90f9e5a6d55f2d01b817d9`.
The unchanged `neurips_2026.sty` text is embedded with `filecontents*` in the
existing canonical source because the native editor compiles a standalone file.
Its SHA256 is `c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a`.
This vendor style adds source lines; it is not a duplicated hand-written style.
The package uses `preprint,nonatbib`, keeping the sole author visible and avoiding
an accepted-conference or under-review notice. Original margin/font overrides
were removed. References precede appendices; the full grading table and duplicate
document plot are now supplementary. The native compiler reports success.

All 29 bibliography keys are unique and cited, with no unresolved citation keys.
Rendered body-page count remains unverified; this is not a claim of nine-page
main-track compliance. A separate 16-item voluntary readiness audit is now recorded in
[NEURIPS_CHECKLIST_READINESS_2026-09-30.md](NEURIPS_CHECKLIST_READINESS_2026-09-30.md);
the official full checklist is not included in this workshop PDF. Use the requirements above as an editing/rigor target and retain
these remaining formal checks explicitly.
Detailed original model-collection history is now in an appendix, with a concise
protocol summary in the body. The completed Gemma replication has a separate
appendix/table; its discovery status and amendments remain explicit.

## Transparency appropriate to the experiment

The main-track checklist is useful as a voluntary rigor audit here. State which
claims are exploratory, what the reference certifies, runtime/backend settings,
failure denominators, source licenses/access limits, and replay versus fresh
inference requirements. Describe substantive AI-assisted review/analysis methods
and their correlated-error limits. No human expert review, learned repair or
downstream financial loss has been measured. Author responsibility remains with
Sebastian Böhler; AI tools are not authors.

The public CFP does not require a separate broader-impact heading. A concise
discussion can explain that misgraded financial quantities can distort an
evaluation, while avoiding unsupported deployment/trading-loss claims.
