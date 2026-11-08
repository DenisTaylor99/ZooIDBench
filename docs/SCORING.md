# Scoring and taxonomic policy

## Primary point rubric

| Prediction outcome | Points |
|---|---:|
| Wrong genus, no usable genus answer, or abstention | 0 |
| Correct genus with an explicitly wrong species | 0.5 |
| Correct genus only, without species-level selection | 1 |
| Correct species plus explicitly wrong subspecies (when reference subspecies exists) | 1.5 |
| Correct species, without a correct subspecies identification | 2 |
| Correct species and correct verified subspecies | 3 |

The scoring maximum is **2 for each of 22 species-only specimens** and **3 for each of eight subspecies-bearing specimens**, totaling **68 per condition per model**. An additional **−0.5 penalty** applies to adjudicated fabricated scientific names, floored at zero. Wrong but existing taxa are not automatically "fabrications". The same reference maxima apply to both conditions even when the image-only photo cannot support a subspecies.

Because species-only specimens are capped at 2, extra subspecies assertions cannot increase their primary score. **The primary score does not measure the accuracy of every subspecies-status assertion.**

## Adjudication

- Current accepted taxon names and documented historical combinations were credited under the pilot's pre-existing policy; e.g., *Morelia amethistina* for *Simalia amethistina*, *Bothrochilus albertisii* for *Leiopython albertisii*.
- The pilot explicitly awarded species-level credit to the former broad *Boiga dendrophila* treatment (including *B. d. melanota*) for *Boiga melanota*, without extra subspecies credit. The former broad classification is taxonomically less precise than the current label.
- *Azemiops kharini* was credited as *A. feae* under the pilot's synonym adjudication.
- Unsupported taxonomic recombinations were evaluated separately from documented historical synonyms; see **Fabricated names** below and the `fabricated_name` column in both scored CSVs.
- Where the model explicitly corrected itself within the same answer, the **final identification** was scored, and the raw output preserved. Examples include Claude Sonnet 5.5's location-condition answers to images 002 and 023.
- In the location condition, Claude Haiku 5.5 twice inferred two snakes from one photographed snake (images 006 and 012). The experimenter specified **score 0, no fabricated-name penalty** for each. This is a special manual rule and is visibly flagged.
- Some answers mention tentative species while committing only to a genus. The parser uses explicit overrides; review those decisions before comparing species-attempt rates.
- Outdated *genus-only* names were generally not given current-genus credit merely because they formerly contained the taxon; this policy differs from accepting a complete unambiguous historical combination. 

## Fabricated names

A name counts as fabricated when the combination never existed as a valid or historical scientific name, even if its parts are real. This is different from a documented historical synonym, which is credited (see above). Three answers were adjudicated as fabricated and received the −0.5 penalty, floored at zero:

| Condition | Model | Image | Ground truth | Answer | Reason |
|---|---|---|---|---|---|
| Image only | GPT-6.1 Sol | 016 | *Zamenis situla* | *Zamenis leopardinus* | The historical name for this species is *Coluber leopardinus*; the combination *Zamenis leopardinus* was never used. Scored 0.5 (correct genus, wrong species) − 0.5 = **0**. |
| + location | Gemini 3.5 Flash-Lite | 019 | *Malayopython timoriensis* | *Simalia clarki* | The historical name is *Liasis clarki*; the combination *Simalia clarki* was never used. Already 0 (wrong genus), so the penalty has no numerical effect. |
| + location | Gemini 3.5 Flash-Lite | 025 | *Thamnophis sirtalis infernalis* | *Thamnophis sirtalis trifasciatus* | No such recognized subspecies. Scored 1.5 (correct species, wrong subspecies) − 0.5 = **1**. |

The *Zamenis leopardinus* case is the only one that changes a ranking-relevant total: crediting it as a synonym would raise GPT-6.1 Sol's image-only score from 41 to 43. Because the epithet refers to the correct species, a reader could reasonably argue for that alternative; the pilot applies the stricter rule that only combinations that actually existed are credited.

## Sensitivity scores

The `score_no_specificity_penalty` analysis restores genus-only credit to a correct-genus/wrong-species answer (0.5 → 1) and restores the full species-only score to a correct-species/wrong-subspecies answer (1.5 → 2). It **retains the fabricated-name deduction** unless a separate sensitivity analysis removes fabrication penalties too. Any future analysis must apply both changes consistently.

## Confidence and secondary measures

Species-level **accuracy** = correct species / 30. **Coverage** = responses attempting a species / 30. **Selective accuracy** = correct species / attempted species; this is not equivalent to overall accuracy. **High-confidence precision** = correctly identified species with the species-confidence field `High` / all species attempts with that confidence. If there are zero such predictions (as in one image-only run), it shows **N/A**.

## Caution on automatic scoring

`code/score_zooid.py` reads the ground truth from `data/specimens_public.csv`, but its taxonomic aliases and named overrides are specific to this pilot. Its regex and canonicalization are not a universal solution for scientific names or complex free-text responses. Raw outputs and manual adjudication remain necessary.
