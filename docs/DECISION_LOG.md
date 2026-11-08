# Decision log 

## Established decisions

- Two conditions, seven models, 30 photographs in fixed randomized order; the second condition adds a locality string to each image.
- Original prompt blocks preserved in `PROMPTS.md`; model labels randomized between conditions.
- Partial-credit denominator 68; incorrect species and incorrect subspecies reduce the score while correct genus/species still receive credit.
- Historical synonym policy credited *Morelia amethistina*, *Azemiops kharini*, *Bothrochilus albertisii*, *Maticora bivirgata* and former broad *Boiga dendrophila* combinations as documented in the scoring instructions.
- Fabricated names are combinations that never existed as valid or historical names. Three were adjudicated (details in `SCORING.md`):
  - Image-only GPT-6.1 Sol, img_016: *Zamenis leopardinus* (the historical name is *Coluber leopardinus*); penalty applied, final score 0.
  - Location Gemini 3.5 Flash-Lite, img_019: *Simalia clarki* (the historical name is *Liasis clarki*); already 0, so no numerical effect.
  - Location Gemini 3.5 Flash-Lite, img_025: *Thamnophis sirtalis trifasciatus* (no such recognized subspecies); final score 1.
- Location Claude Haiku 5.5's false two-snake identifications (img_006 and img_012) each score zero, **without** fabrication penalty.
- Explicit self-corrections in an answer count as the final identification (notably location-condition Claude Sonnet 5.5, images 002 and 023).

## Changes made for publication

- Response files were renamed from blind letters to model names, for transparency. Adjudication was done under the blind labels; the mapping is in `MODELS_AND_ENVIRONMENTS.md` and in the `blind_label` column of the scored CSVs.

## Contamination and exclusion

Work source references in preliminary GPT-6.1 Sol and GPT-6 Astra sessions pointed at earlier snake-identification conversations and matching photos. Those trials are **not included** in published scoring. The observation supports cross-conversation retrieval/benchmark contamination; it does not establish intentional reward hacking. Two image + location attempts by Gemini 3.5 Flash-Lite in the Gemini app were also excluded, because the model searched the web in both; the run was repeated in Google AI Studio.
