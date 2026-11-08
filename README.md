# ZooIDBench - Snake ID pilot (v0.1.0)

**Not a peer-reviewed benchmark or a claim of general-purpose zoological competence.**

On social media, people often post screenshots of chats in which they ask an AI model, such as GPT, Gemini or Claude, to identify an animal they found. This is usually done on the assumption that the model can identify it reliably. However, these are general-purpose models, not designed or evaluated specifically for species identification, and their accuracy at it has not been established.

**ZooIDBench - snake ID pilot (v0.1.0)** tests whether seven multimodal language models can identify **30 photographed snakes** at genus, species, and (when applicable) subspecies rank. Every model was evaluated under two conditions: **photograph only**, and **the same photograph plus a geographic locality**. The questions are how accurate these vision-language models (VLMs) are at identification, and how much providing a location changes their accuracy, coverage, and expressed confidence.

The models were tested **in their consumer chat apps**, deliberately: that is how most people actually ask an AI to identify an animal. The results therefore describe what a user of these products would have received, not the behaviour of the underlying models under controlled API settings.

**Main descriptive result:** mean species identification accuracy across models increased from **45.2%** to **72.4%** (**+27.1 percentage points**). Mean normalized partial-credit score rose from **48.2%** to **72.3%** (**+24.1 percentage points**). These figures describe this particular sample, not an estimated population-wide effect.

## Models and outcomes

| Model                 |      Image only | Image + locality | Score gain | Species correct: image only | Species correct: + locality |
| --------------------- | --------------: | ---------------: | ---------: | --------------------------: | --------------------------: |
| GPT-6 Astra           |   43/68 (63.2%) |  63.5/68 (93.4%) |   +30.1 pp |                       17/30 |                       28/30 |
| GPT-6.1 Sol           |   41/68 (60.3%) |    63/68 (92.6%) |   +32.4 pp |                       17/30 |                       27/30 |
| Claude Opus 5.5       | 46.5/68 (68.4%) |  62.5/68 (91.9%) |   +23.5 pp |                       20/30 |                       28/30 |
| Claude Sonnet 5.5     | 37.5/68 (55.1%) |    49/68 (72.1%) |   +16.9 pp |                       15/30 |                       21/30 |
| GPT-6 Luna            | 15.5/68 (22.8%) |    40/68 (58.8%) |   +36.0 pp |                        6/30 |                       18/30 |
| Gemini 3.5 Flash-Lite |   31/68 (45.6%) |    39/68 (57.4%) |   +11.8 pp |                       14/30 |                       19/30 |
| Claude Haiku 5.5      |   15/68 (22.1%) |    27/68 (39.7%) |   +17.6 pp |                        6/30 |                       11/30 |

The normalized score is **points earned / 68 possible points × 100**. It is not interchangeable with percent of species correctly identified. Rows are sorted by the image + locality score. The top three models with locality (Astra, Sol, Opus) are within one point of each other, and 30 images cannot establish an order among them.

The tested line-ups are **not balanced across families**. Both OpenAI and Anthropic offer four tiers; this pilot includes OpenAI’s top, second and smallest tiers (GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna) but Anthropic’s second, third and smallest (Claude Opus 5.5, Sonnet 5.5, Haiku 5.5). Comparisons between families should therefore be made tier by tier, not by averaging each family’s results.

**Gemini 3.5 Flash-Lite is a small, low-cost model, not Google's flagship model.** Its results should not be read as describing "Gemini" in general. The same applies to the smaller models of the other families (Claude Haiku 5.5, GPT-6 Luna).

## Read first

- [Study design and administration](docs/METHODOLOGY.md)
- [Results and interpretation](docs/RESULTS.md)
- [Exploratory analyses: paired tests, regressions, calibration, safety-relevant errors](docs/EXPLORATORY_ANALYSES.md)
- [Scoring and taxonomic adjudication](docs/SCORING.md)
- [Models, environments, and sources of variation](docs/MODELS_AND_ENVIRONMENTS.md)
- [Preselected visual challenges and qualitative errors](docs/QUALITATIVE_FINDINGS.md)
- [Caveats and threats to validity](docs/LIMITATIONS.md)
- [Reproducibility, data and code](docs/REPRODUCIBILITY.md)
- [Image provenance and licenses](docs/IMAGE_SOURCES_AND_LICENSES.md)
- [Original standardized prompts](docs/PROMPTS.md)
- [Decisions log](docs/DECISION_LOG.md)

## Repository contents

- `data/specimens_public.csv` — answer key read by the scorer: specimen IDs, ground truth, taxonomic groups, maximum scores, and the **locality text exactly as sent to the models**; must not be disclosed to models during a future blind run.
- `data/ORIGINAL_SPECIMEN_REGISTRY.md` — source registry with observer evidence, identifiability notes and licensing entries.
- `data/responses/` — the 14 original model-response transcriptions, one per model per condition, named after the model (for example `image_only/GPT-6 Astra.md` and `image_plus_location/GPT-6 Astra_location.md`).
- `data/image_only_responses_scored_210.csv`, `data/location_responses_scored_210.csv` — **210-row** scored datasets, one row per model per image, with model names, blind labels, raw answers, adjudications and scores.
- `data/image_only_summary.csv`, `data/location_summary.csv` — per-model aggregate metrics for each condition.
- `data/image_only_adjudications.csv`, `data/location_adjudications.csv` — every manually adjudicated or annotated answer.
- `data/paired_per_image.csv`, `data/paired_model_summary.csv` — item-level and model-level comparison of the two conditions, including exact McNemar tests.
- `code/score_zooid.py` — Python scorer that reads the answer key from `data/specimens_public.csv` and regenerates all the CSVs above from the response files. Its synonym list and manual adjudications are specific to this pilot and are kept in one marked section of the script; replace them before reusing it on another dataset (see [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)).
- `figures/` — illustrative graphics, generated by `code/make_figures.py`; the CSVs, not the figures, are the authoritative numeric source.

**Images are not included** in this preliminary release bundle. Source observations and photographer/license details are recorded in the registry. Redistributing a derivative dataset requires honoring each individual photograph's license and attribution terms; consult [image provenance](docs/IMAGE_SOURCES_AND_LICENSES.md).

## Who did what

- **Benchmark design, image selection, prompts, data collection, ground truth, and all adjudication decisions:** the author of this repository.
- **Original scoring script and first analysis:** GPT-5.6 Sol (OpenAI), used as an assistant through ChatGPT.
- **Review of the scoring script, bug fixes, re-scoring of both conditions, paired analysis, figure script and charts, and documentation review:** Claude Opus 5.5 (Anthropic), used as an assistant through Claude.ai.
- **Documentation drafts:** written with GPT-5.6 Sol and Claude Opus 5.5, then checked and edited by the author.

**Assistant use note.** Both assistant model families are among the tested models, and the reviewing assistant, Claude Opus 5.5, is the same model as one of the seven tested. The assistant GPT-5.6 Sol is a different version from the tested GPT-6.1 Sol. To limit any possible bias:

- the scoring rubric is mechanical (fixed points for genus, species and subspecies, plus documented penalties), not a judgement of answer quality;
- adjudication decisions were made by the author, with model identities hidden behind letters A–G that were reshuffled between conditions;
- all raw answers, adjudications and code are public, so anyone can check that no rule favours a particular model.

**Responsibility note**. The author is not a programmer or herpetologist, and the scripts were written entirely by AI assistants. The code may therefore contain mistakes, and some ground-truth identifications could be wrong. Any mistakes remain the author's responsibility.

## What the pilot does not establish

This is a convenience-selected, taxonomically heterogeneous dataset of 30 images, with two conditions run in separate multi-image chats per model. It is not representative of snakes in the wild, and it does not isolate geographic prior knowledge from all other session effects. Scores should not guide identification of dangerous snakes in real-world safety decisions.

## Future versions

- **Repeated runs**, to measure how much the answers vary when the same model sees the same photograph again, ideally with each photograph in a new conversation and the images in a different order for each run.
- **Balanced model line-ups**: all four tiers of each family, including GPT Terra and Claude Fable.
- **Other animal groups**, starting with spiders.
- **A new, unpublished image set**, since the photographs and answers in this release are now public and could reach future models' training data.
- **A fuller record of each run**: exact model versions, settings and image files, so a run can be repeated as closely as possible.

## Citation and licensing

**Citation.** Please cite this repository by its name, version and URL: ZooIDBench - Snake ID pilot (v0.1.0), 2026, https://github.com/DenisTaylor99/ZooIDBench

**Licensing.** The scoring code is released under the MIT License (see `LICENSE`). Documentation and data files are released under CC BY 4.0. The photographs are not included in this repository; each remains under its photographer’s own license, as recorded in `data/ORIGINAL_SPECIMEN_REGISTRY.md`.
