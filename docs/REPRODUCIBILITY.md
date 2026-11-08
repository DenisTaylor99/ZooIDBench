# Data, scoring code, and reproducibility

## Files

- `docs/PROMPTS.md`: exact experiment prompts and per-image message templates.
- `data/specimens_public.csv`: the answer key read by the scorer. One row per image, with the ground-truth species, the verified subspecies (or `none`), the taxonomic group, the locality string exactly as sent to the models, and the maximum score.
- `data/responses/image_only/<Model name>.md`: preserved verbatim answer transcriptions, image-only condition.
- `data/responses/image_plus_location/<Model name>_location.md`: preserved verbatim answer transcriptions, image + location condition.
- `data/image_only_responses_scored_210.csv`, `data/location_responses_scored_210.csv`: one row per model per image, including model name, blind label, raw response, parsed and adjudicated identification, alias flag, confidence fields, validity flags, scoring category and score.
- `data/image_only_adjudications.csv`, `data/location_adjudications.csv`: every manually adjudicated or annotated answer.
- `data/image_only_summary.csv`, `data/location_summary.csv`: per-model aggregate metrics.
- `data/paired_per_image.csv`, `data/paired_model_summary.csv`: item-level and model-level comparison of the two conditions, including exact McNemar tests.
- `code/score_zooid.py`: scorer that regenerates all the CSVs above from the response files.
- `code/make_figures.py`: script that redraws the four charts in `figures/` from the CSVs above (requires matplotlib).
- `figures/`: the four charts, numbered in the order they appear in `RESULTS.md`.

The letter labels (A–G) used during blind adjudication are mapped to model names in `docs/MODELS_AND_ENVIRONMENTS.md` and in the `blind_label` column of every scored CSV.

## Reproduce the scoring

Use Python 3 with the standard library only. From the repository root, run:

```bash
python code/score_zooid.py
```

The script reads the answer key and the 14 response files, scores both conditions, and overwrites the eight CSVs in `data/`. It checks the validation invariants below and stops with an error if any fails. The answer key is not written in the script; the synonym policy and the manual adjudications are, in one marked section, and should be inspected before altering. The script does **not** independently identify snakes or validate an iNaturalist ground-truth record.

To redraw the figures from the new CSVs, install matplotlib (`pip install matplotlib`) and run:

```bash
python code/make_figures.py
```

It overwrites the four PNG files in `figures/`. Everything plotted is read from the CSVs; only the chart wording (titles, footnotes and the order of the taxonomic groups) is set in a short section at the top of the script.

## Using the scorer on another dataset

1. Replace `data/specimens_public.csv` with a new answer key in the same format. The scorer uses the columns `image` (`img_NNN.ext`), `ground_truth_species` (a binomial), `verified_subspecies` (a trinomial or `none`), `taxonomic_group` and `max_score` (3 with a verified subspecies, otherwise 2); other columns are ignored.
2. Put the response files in `data/responses/image_only/<Model name>.md` and `data/responses/image_plus_location/<Model name>_location.md`. Each file needs one `### img_NNN.ext` heading per image, followed by the answer in the format requested in `PROMPTS.md`.
3. In the script's section marked "Dataset-specific adjudications", replace the blind labels and model order, and replace or empty the synonym list, overrides and fabricated-name decisions.
4. Run `code/make_figures.py` to draw the charts, after adjusting the wording section at the top of that script (for example, the name of the animal group and the list of taxonomic groups).

The output file names include the number of scored rows (models × images), for example `_scored_210` here.

## Validation invariants

- Seven × 30 = **210 rows per condition**.
- All 30 `img_001`–`img_030` entries appear once per model per condition.
- Every image in the answer key has a maximum of 3 if it has a verified subspecies and 2 otherwise; here eight maxima of 3 + 22 maxima of 2 = **68** per model.
- Scores lie between 0 and the item's maximum.
- If subspecies is correct, species must be correct; if species is correct, genus must be correct.
- Image-only and location conditions map letters to model names **differently**; see the mapping table.
- Fabrication and false-two-specimen flags must be preserved through re-runs.

## Current reproducibility boundaries

Both conditions are fully scored from the raw responses by a single command, and the totals match the audited values (image only: Haiku 15, Astra 43, Gemini 31, Sonnet 37.5, Opus 46.5, Luna 15.5, Sol 41; image + location: Luna 40, Gemini 39, Sol 63, Haiku 27, Opus 62.5, Astra 63.5, Sonnet 49).

What cannot be reproduced exactly is the models' behaviour itself. The original processed image files are **not in this release bundle**; the specimen/source registry can be used to recover or request them subject to licenses. Model build identifiers and inference parameters were not recorded, and consumer apps change over time, so re-running the same prompts today may give different answers.


