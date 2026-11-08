# Exploratory analyses

These analyses go beyond the primary descriptive results in [RESULTS.md](RESULTS.md). They are **exploratory**: they were not pre-specified, the sample is 30 images with one run per model and condition, and no correction for multiple comparisons has been applied. Treat them as hypothesis-generating.

All numbers are computed by `code/score_zooid.py` from `data/image_only_responses_scored_210.csv`, `data/location_responses_scored_210.csv`, `data/paired_per_image.csv` and `data/paired_model_summary.csv`.

## 1. Paired effect of location, per model

Each model answered the same 30 images in both conditions, so the comparison is paired. For species-level correctness, the exact McNemar test compares the images that became correct with location against those that stopped being correct.

| Model | Species correct: image only → + location | Became correct | Stopped being correct | Exact McNemar *p* |
|---|---:|---:|---:|---:|
| GPT-6 Astra | 17 → 28 | 11 | 0 | 0.001 |
| GPT-6.1 Sol | 17 → 27 | 10 | 0 | 0.002 |
| GPT-6 Luna | 6 → 18 | 14 | 2 | 0.004 |
| Claude Opus 5.5 | 20 → 28 | 8 | 0 | 0.008 |
| Claude Sonnet 5.5 | 15 → 21 | 7 | 1 | 0.070 |
| Claude Haiku 5.5 | 6 → 11 | 6 | 1 | 0.125 |
| Gemini 3.5 Flash-Lite | 14 → 19 | 7 | 2 | 0.180 |

For four models, the improvement with location is unlikely to be explained by chance variation between the two runs. For the other three, the direction is the same but the evidence is weaker. With seven tests, the threshold of 0.05 should not be read as a sharp line, and these *p*-values do not account for run-to-run variability, which was not measured.

Gemini 3.5 Flash-Lite's two conditions were run in different interfaces (the Gemini app for image only, Google AI Studio for image + location; see [MODELS_AND_ENVIRONMENTS.md](MODELS_AND_ENVIRONMENTS.md)). Its paired differences, in this section and in those below, may therefore reflect the change of interface as well as the added location.

## 2. Answers that got worse with location

Every model improved overall, but at the item level **11 answers lost points** when the location was added. All 11 came from the four lower-scoring models; Astra, Sol and Opus had none.

| Model | Image | Ground truth | Image only | + location |
|---|---|---|---|---|
| Claude Sonnet 5.5 | 017 | *Acanthophis rugosus* | *Acanthophis* (1) | *Acanthophis pyrrhus* (0.5) |
| Claude Sonnet 5.5 | 024 | *Leiopython albertisii* | *Leiopython albertisii* (2) | *Leiopython* (1) |
| GPT-6 Luna | 021 | *Aspidites ramsayi* | *Aspidites ramsayi* (2) | *Pseudechis australis* (0) |
| GPT-6 Luna | 027 | *Tropidolaemus wagleri* | *Tropidolaemus wagleri* (2) | *Boiga dendrophila* (0) |
| GPT-6 Luna | 028 | *Eunectes notaeus* | *Eunectes* (1) | *Eunectes murinus* (0.5) |
| Gemini 3.5 Flash-Lite | 008 | *Nerodia fasciata confluens* | *Nerodia fasciata* (2) | *Nerodia erythrogaster* (0.5) |
| Gemini 3.5 Flash-Lite | 020 | *Thamnophis sirtalis tetrataenia* | *Thamnophis sirtalis* (2) | *T. s. infernalis* (1.5) |
| Gemini 3.5 Flash-Lite | 025 | *Thamnophis sirtalis infernalis* | *Thamnophis sirtalis* (2) | *T. s. trifasciatus* (1, fabricated name) |
| Gemini 3.5 Flash-Lite | 028 | *Eunectes notaeus* | *Eunectes notaeus* (2) | *Eunectes murinus* (0.5) |
| Claude Haiku 5.5 | 013 | *Naja samarensis* | *Naja* (1) | *Naja philippinensis* (0.5) |
| Claude Haiku 5.5 | 028 | *Eunectes notaeus* | *Eunectes notaeus* (2) | *Eunectes murinus* (0.5) |

A recurring pattern is a location **overriding correct visual evidence** in favour of the best-known species of the region. The clearest case is image 028: three models correctly identified the yellow anaconda (or its genus) from the photograph alone, then switched to the green anaconda (*E. murinus*) when told it was photographed in Mato Grosso, Brazil, even though the yellow pattern is visible. Location also pushed some models into adding subspecies they could not support (020, 025). This is consistent with weaker models treating location as stronger evidence than the image, despite the prompt instruction to treat location as "useful evidence, not definitive proof".

## 3. Calibration: wrong answers given with high confidence

High-confidence errors are the most misleading kind for a user. Each model rated its confidence separately for the genus and, when it named one, for the species. The table counts, for each condition, how many answers a model rated `High` and how many of those were wrong. Each condition has 30 answers per model; every answer has a genus confidence, but only answers that name a species have a species confidence, so the two columns have different totals.

Each cell reads **wrong / rated `High`**. For example, Gemini 3.5 Flash-Lite's "7 / 25" for species with location means that it named a species with `High` confidence in 25 of its 30 answers, and the species was wrong in 7 of those.

| Model | Species, image only | Species, + location | Genus, image only | Genus, + location |
|---|---:|---:|---:|---:|
| GPT-6 Astra | 2 / 13 | 0 / 27 | 4 / 27 | 0 / 29 |
| GPT-6.1 Sol | 2 / 15 | 1 / 26 | 3 / 26 | 0 / 30 |
| Claude Opus 5.5 | 0 / 10 | 0 / 16 | 0 / 21 | 0 / 27 |
| Claude Sonnet 5.5 | 0 / 8 | 1 / 10 | 2 / 21 | 1 / 23 |
| GPT-6 Luna | 3 / 4 | 3 / 15 | 4 / 6 | 5 / 22 |
| Gemini 3.5 Flash-Lite | 2 / 7 | 7 / 25 | 7 / 26 | 6 / 30 |
| Claude Haiku 5.5 | N/A (0 rated `High`) | 1 / 4 | 2 / 4 | 3 / 15 |

- **Claude Opus 5.5** made no high-confidence errors in either condition, at either rank. It also rated fewer species answers `High` than GPT-6 Astra or GPT-6.1 Sol.
- **GPT-6 Astra and GPT-6.1 Sol** made a few high-confidence errors from the image alone, and almost none with location (one wrong species for Sol), while rating nearly all of their answers `High`.
- **Gemini 3.5 Flash-Lite** made the most high-confidence genus errors in both conditions. With location it rated far more species answers `High` (7 → 25), but the share of them that were correct stayed about the same (71% → 72%), so its confident wrong species rose from 2 to 7.
- **GPT-6 Luna** rarely used `High` from the image alone, but when it did, it was usually wrong (3 of 4 species, 4 of 6 genera).
- **Claude Haiku 5.5**, despite the lowest scores, rarely used `High` confidence: never for a species from the image alone, and four times with location. Most of its errors were therefore flagged as uncertain.

The confidence scale is ordinal and self-reported, so these figures describe how often each label was trustworthy in this sample; they are not calibration curves.

## 4. Venomous snakes identified as non-dangerous genera

From a safety perspective, the worst error is identifying a medically significant venomous snake as a genus that is harmless or of negligible medical importance. The table lists every such case, both conditions, with the stated **genus** confidence.

| Model | Condition | Ground truth | Identified as | Genus confidence |
|---|---|---|---|---|
| Gemini 3.5 Flash-Lite | image only | *Azemiops feae* | *Sibon annulatus* | High |
| Gemini 3.5 Flash-Lite | image only | *Protobothrops flavoviridis* | *Leptodeira annulata* | High |
| Gemini 3.5 Flash-Lite | image only | *Bungarus flaviceps* | *Clelia clelia* | Medium-High |
| Gemini 3.5 Flash-Lite | + location | *Bungarus flaviceps* | *Cylindrophis ruffus* | High |
| Gemini 3.5 Flash-Lite | + location | *Azemiops feae* | *Sibynophis chinensis* | High |
| GPT-6 Luna | + location | *Bungarus flaviceps* | *Cylindrophis ruffus* | High |
| GPT-6 Luna | + location | *Tropidolaemus wagleri* | *Boiga dendrophila* | High |
| GPT-6 Luna | image only | *Protobothrops flavoviridis* | *Morelia spilota* | Medium-High |
| GPT-6 Luna | + location | *Azemiops feae* | *Euprepiophis mandarinus* | Medium-High |
| GPT-6 Luna | + location | *Acanthophis rugosus* | *Aspidites ramsayi* | Medium |
| GPT-6 Astra | image only | *Bungarus flaviceps* | *Oxyrhopus formosus* | High |
| GPT-6 Astra | image only | *Protobothrops flavoviridis* | *Morelia spilota* | High |
| GPT-6.1 Sol | image only | *Protobothrops flavoviridis* | *Morelia spilota* | High |
| GPT-6.1 Sol | image only | *Bungarus flaviceps* | *Oxyrhopus formosus* | Medium-High |
| Claude Sonnet 5.5 | + location | *Protobothrops flavoviridis* | *Elaphe carinata* | High |
| Claude Sonnet 5.5 | image only | *Protobothrops flavoviridis* | *Chilabothrus striatus* | Medium-High |
| Claude Sonnet 5.5 | image only | *Bungarus flaviceps* | *Oxyrhopus* | Low-Medium |
| Claude Sonnet 5.5 | + location | *Azemiops feae* | *Dinodon* | Low |
| Claude Opus 5.5 | + location | *Bungarus flaviceps* | *Gonyophis margaritatus* | Medium-High |
| Claude Opus 5.5 | image only | *Protobothrops flavoviridis* | *Leioheterodon madagascariensis* | Medium |
| Claude Opus 5.5 | image only | *Bungarus flaviceps* | *Oxyrhopus* | Low-Medium |
| Claude Opus 5.5 | image only | *Azemiops feae* | *Lycodon* | Low-Medium |
| Claude Haiku 5.5 | + location | *Protobothrops flavoviridis* | *Elaphe carinata* | Medium |
| Claude Haiku 5.5 | image only | *Protobothrops flavoviridis* | *Morelia* | Low-Medium |
| Claude Haiku 5.5 | + location | *Agkistrodon taylori* | *Lampropeltis* | Low-Medium |

Counting only errors made with `High` genus confidence: Gemini 3.5 Flash-Lite 4, GPT-6 Luna 2, GPT-6 Astra 2, GPT-6.1 Sol 1, Claude Sonnet 5.5 1, Claude Opus 5.5 0, Claude Haiku 5.5 0.

Caveats:

- The grouping of genera into "non-dangerous" is the experimenter's own classification for this analysis, not part of the scoring rubric. Some of these genera (for example *Boiga*, *Oxyrhopus*) are rear-fanged and mildly venomous, but are not generally considered medically significant.
- The venomous species differ greatly in danger. A banded or red-headed krait (*Bungarus*) or a habu (*Protobothrops flavoviridis*) is far more dangerous than a snake whose bites cause mainly local effects. 

These results are a reason not to rely on any of the tested models to decide whether a snake is safe to approach or handle. Before handling or approaching any kind of snake you cannot safely identify, always ask a human expert first. 
