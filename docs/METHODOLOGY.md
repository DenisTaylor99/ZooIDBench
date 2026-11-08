# Methodology

## Research question

How accurately can vision-language models (VLMs) identify animals from photographs, and does their accuracy change when the same photograph is accompanied by an explicitly stated geographic locality? This pilot addresses the question for snakes only; later versions are intended to extend it to other groups, such as spiders.

## Sample and selection

The pilot used **30 photographs**, representing **29 distinct species and two recognized subspecies of *Thamnophis sirtalis***. By the locked scoring registry, there are **eight subspecies-bearing entries** and 22 species-only entries. Taxonomic groups were curated to include seven colubrids, six vipers, seven elapids, five pythons, and five boas. These are study-defined bins, not a balanced random sample of snake diversity.

Pictures were sourced from iNaturalist observations. The author selected animals/photos to vary visual distinctiveness, similarity across taxa, geographic distribution, perceived identifiability, and challenging contexts. The rationale for each deliberately challenging image is given in `QUALITATIVE_FINDINGS.md`, and the registry records, for every image, the rank the author judged identifiable with and without location. Labels and geographic details are in `data/specimens_public.csv` and the original specimen registry.

Taxonomy follows The Reptile Database (accessed October 2026), with the exceptions documented in `data/ORIGINAL_TAXONOMY_NOTES.md`.

## Conditions and unit of analysis

1. **Image only:** the model received one processed photograph at a time; no locality text was supplied.
2. **Image + locality:** the model received the same photograph together with the locality string alone (for example `Gosford, New South Wales, Australia`). The exact string sent for each image is listed in `data/specimens_public.csv`. 

Each model had a **fresh, independent chat per condition**. Within a condition, all 30 photographs were sent sequentially, one per message. Models could therefore retain normal within-chat context from earlier turns; the prompt instructed them not to use previous guesses as evidence. This is *not* 30 independent, stateless API requests. All models used the same locked image order (`img_001` through `img_030`), generated from seed `20261011`. The order was randomized once and then kept the same for every model and both conditions. This makes the runs comparable, but any effect of position in the conversation (for example, earlier images influencing later ones) falls on the same images for every model and cannot be separated from the difficulty of those images.

The original prompt text is preserved *verbatim* in [PROMPTS.md](PROMPTS.md). Models were not told their scores or that they were competing. The taxon labels shown in the response-transcription headings were **added to the analysis files** and were not supplied in the prompt or image message.

## Inputs and preparation

Local copies of the images were renamed to opaque `img_NNN` filenames, and their metadata was removed with ExifTool. Finalized files comprised **29 JPEGs and one PNG (`img_001.png`)**. Original files were preserved separately.

The localities were derived from the specimen registry, generally at municipality, district or county granularity, and written out with English administrative names and full country names. They were not randomly generated. The strings actually sent to the models are recorded verbatim in `data/specimens_public.csv`.

## Elicitation and recording

Both prompts requested mandatory genus; species and subspecies only when supportable; a separate subspecies-status field; ordinal confidence (Low, Low-Medium, Medium, Medium-High, High) at each identified rank; and a 1–3 sentence evidence description. Models were instructed not to use searches, databases, code, reverse-image search, or other external tools. Memory and web search were disabled wherever the interface allowed it. The Gemini app does not allow web search to be disabled; how this was handled is described in `MODELS_AND_ENVIRONMENTS.md` and under **Exclusions** below.

The original model answers were copied directly from each chat into Markdown files, unchanged apart from the added `### img_NNN` headings. They were subsequently parsed and adjudicated for scoring. Qualitative descriptions, confidence, and alternative names were retained in the original files and in the `raw_section` field of both scored CSVs. The study deliberately tested answers in **consumer-facing chat interfaces**, because that is where most people ask models to identify animals; the trade-off is that reproducibility is limited by provider behavior and settings (see `MODELS_AND_ENVIRONMENTS.md`).

## Statistical approach

The primary endpoint is the mean **normalized partial-credit score**, computed from each 30-item total and divided by the same maximum of 68 in both conditions. Species accuracy is correct species / 30 (including accepted taxonomy equivalents), not correct / attempts; species attempt coverage and correct / attempted are separate secondary metrics. Genus accuracy and exact subspecies accuracy (out of eight reference subspecies) are also reported. High-confidence precision is correct species among those predictions whose *species-confidence* field says `High`.

Paired within-model changes are primarily **descriptive**. As an exploratory addition, exact McNemar tests on species-level correctness compare the two conditions within each model; they are reported in [EXPLORATORY_ANALYSES.md](EXPLORATORY_ANALYSES.md), without correction for multiple comparisons. No model-rank confidence intervals or out-of-sample generalization claims have been made. The dataset includes correlated visual difficulty and does not estimate prevalence-weighted accuracy.

## Exclusions and interruptions

Earlier Work-interface attempts by GPT-6.1 Sol and GPT-6 Astra exposed **cross-conversation Memory-source links** to previous snake-ID chats and previously submitted photos. Those preliminary contaminated attempts were excluded and rerun in new chats. The source-panel observation demonstrates prior-conversation retrieval, not that the models intentionally cheated or how individual predictions were influenced.

Two attempts at the image + location run of Gemini 3.5 Flash-Lite in the Gemini app were also excluded, because in both the model searched the web despite the instruction not to. The run was then repeated in Google AI Studio, where web search can be disabled. The image-only Gemini run, in the Gemini app, showed no web searches and was kept.
