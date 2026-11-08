# Snake identification pilot — standardized prompts

Each model was tested in two fresh, independent chats: one for **image only** and one for **image + location**. The two conditions were never run in the same chat. The models were not told that they were being compared or how their answers would be scored. All models received the images **in the same predetermined order** in both conditions, and no file name or other text revealed the taxon.

## Prompt A — Image only

This text was sent as the first message of each image-only chat. The 30 images then followed in the locked order, one per message, with no accompanying text.

```text
Snake identification task

You will receive photographs of snakes, one at a time. Identify each specimen as accurately and precisely as the available visual evidence permits, using your existing knowledge.

Identification rules:
1. Provide a scientific genus for every photograph, even if tentative. Provide a species when you can reasonably support one, and a subspecies only when supported. Do not supply additional specificity merely to complete the identification.
2. Prefer a justified broader identification to an unsupported species or subspecies guess. If the photograph is insufficient to distinguish multiple taxa, stop at the most specific supported rank.
3. Do not fabricate scientific names. Use established zoological names to the best of your knowledge. Older scientific names and recognized synonyms are permitted; the evaluation will apply a consistent taxonomy policy.
4. Use only the photograph and your existing knowledge. Do not use web searches, reverse-image searches, databases, code, or other external tools. Do not assume access to the photograph's original filename, metadata, source, or location.
5. Do not assume every species has recognized subspecies. Distinguish between a species with no recognized subspecies and a species with recognized subspecies that cannot be identified from the available evidence. If the species itself is not identified, do not make a claim about its subspecies status.

Confidence ratings:
- Genus confidence: confidence that your stated genus is correct.
- Species confidence: confidence that your stated species is correct, if you provided one.
- Subspecies confidence: confidence that your stated subspecies is correct, if you provided one.
- For each confidence field, use exactly one of: Low, Low-Medium, Medium, Medium-High, High.
- Genus confidence is mandatory. Use N/A for species or subspecies confidence only if you have not identified that rank.
- Do not report an overall-confidence rating or numerical probabilities. Do not inflate confidence to appear decisive.

Use this exact response format:

Identification: [scientific genus, species, or subspecies at the most specific rank supported]
Subspecies status: [Identified: scientific trinomial / Recognized but not identifiable / No recognized subspecies / Undetermined because species is unidentified]
Confidence:
- Genus: [Low / Low-Medium / Medium / Medium-High / High]
- Species: [Low / Low-Medium / Medium / Medium-High / High / N/A]
- Subspecies: [Low / Low-Medium / Medium / Medium-High / High / N/A]
Visual evidence: [1–3 sentences describing observable diagnostic characteristics and important ambiguity. Do not claim to see features that the photograph does not show.]

Treat every image as a separate specimen. Do not infer that successive photographs depict related or different taxa. Do not use earlier guesses as evidence for later photographs. Put your identification and confidence before visual evidence. Do not revise previous responses unless explicitly asked.

Wait for the first image.
```

## Prompt B — Image + location

This text was sent as the first message of each image + location chat. The 30 images then followed in the same order, one per message, each with its locality string in the same message.

```text
Snake identification task — image plus geographic location

You will receive photographs of snakes, one at a time. Each photograph will be accompanied by the geographic location where the specimen was photographed. Identify each specimen as accurately and precisely as the combined visual and location evidence permits, using your existing knowledge.

Identification rules:
1. Provide a scientific genus for every photograph, even if tentative. Provide a species when you can reasonably support one, and a subspecies only when supported. Do not supply additional specificity merely to complete the identification.
2. Prefer a justified broader identification to an unsupported species or subspecies guess. If the photograph and location are insufficient to distinguish multiple taxa, stop at the most specific supported rank.
3. Do not fabricate scientific names. Use established zoological names to the best of your knowledge. Older scientific names and recognized synonyms are permitted; the evaluation will apply a consistent taxonomy policy.
4. Use only the supplied photograph, the explicitly supplied location, and your existing knowledge. Do not use web searches, reverse-image searches, databases, code, or other external tools. Do not assume access to the photograph's original filename, metadata, or source. Treat location as useful evidence, not definitive proof of identity.
5. Do not assume every species has recognized subspecies. Distinguish between a species with no recognized subspecies and a species with recognized subspecies that cannot be identified from the available evidence. If the species itself is not identified, do not make a claim about its subspecies status.

Confidence ratings:
- Genus confidence: confidence that your stated genus is correct.
- Species confidence: confidence that your stated species is correct, if you provided one.
- Subspecies confidence: confidence that your stated subspecies is correct, if you provided one.
- For each confidence field, use exactly one of: Low, Low-Medium, Medium, Medium-High, High.
- Genus confidence is mandatory. Use N/A for species or subspecies confidence only if you have not identified that rank.
- Do not report an overall-confidence rating or numerical probabilities. Do not inflate confidence to appear decisive.

Use this exact response format:

Identification: [scientific genus, species, or subspecies at the most specific rank supported]
Subspecies status: [Identified: scientific trinomial / Recognized but not identifiable / No recognized subspecies / Undetermined because species is unidentified]
Confidence:
- Genus: [Low / Low-Medium / Medium / Medium-High / High]
- Species: [Low / Low-Medium / Medium / Medium-High / High / N/A]
- Subspecies: [Low / Low-Medium / Medium / Medium-High / High / N/A]
Visual evidence: [1–3 sentences describing observable diagnostic characteristics, the relevance of the supplied geographic location, and important ambiguity. Do not claim to see features that the photograph does not show.]

Treat every image as a separate specimen. Do not infer that successive photographs depict related or different taxa. Do not use earlier guesses as evidence for later photographs. Put your identification and confidence before visual evidence. Do not revise previous responses unless explicitly asked.

Wait for the first image.
```

### Per-image message templates

**A — Image only:** the image alone, with no text.

**B — Image + location:** the image plus one line with its locality, in the form:

```text
[locality], [administrative region], [country]
```

A few localities have fewer or more levels (for example `Mandai, Singapore`). The exact string sent for each image is in `data/specimens_public.csv`.

All 30 specimens had a usable locality, so none was excluded from the paired comparison.


