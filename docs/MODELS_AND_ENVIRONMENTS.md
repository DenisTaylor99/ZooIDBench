# Models, interface environments, and configuration

## Models included

Seven named multimodal models were evaluated. During scoring and adjudication, models were identified only by letters A–G, **reshuffled between conditions** to limit identity-based bias.

| Model | Blind label: image only | Blind label: + location | Image-only file | Image + location file |
|---|:---:|:---:|---|---|
| Claude Haiku 5.5 | A | D | `data/responses/image_only/Claude Haiku 5.5.md` | `data/responses/image_plus_location/Claude Haiku 5.5_location.md` |
| GPT-6 Astra | B | F | `data/responses/image_only/GPT-6 Astra.md` | `data/responses/image_plus_location/GPT-6 Astra_location.md` |
| Gemini 3.5 Flash-Lite | C | B | `data/responses/image_only/Gemini 3.5 Flash-Lite.md` | `data/responses/image_plus_location/Gemini 3.5 Flash-Lite_location.md` |
| Claude Sonnet 5.5 | D | G | `data/responses/image_only/Claude Sonnet 5.5.md` | `data/responses/image_plus_location/Claude Sonnet 5.5_location.md` |
| Claude Opus 5.5 | E | E | `data/responses/image_only/Claude Opus 5.5.md` | `data/responses/image_plus_location/Claude Opus 5.5_location.md` |
| GPT-6 Luna | F | A | `data/responses/image_only/GPT-6 Luna.md` | `data/responses/image_plus_location/GPT-6 Luna_location.md` |
| GPT-6.1 Sol | G | C | `data/responses/image_only/GPT-6.1 Sol.md` | `data/responses/image_plus_location/GPT-6.1 Sol_location.md` |

Responses were adjudicated under the blind labels; the files were renamed after the model names only for publication. The scored CSVs contain both the `model_name` and the `blind_label` columns.

## Interface and settings

This pilot used **consumer chat applications** rather than one unified API system. GPT-6 Astra, GPT-6.1 Sol and GPT-6 Luna were accessed through ChatGPT Work, both on mobile and in a web browser. Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 were accessed through Claude.ai chat, both on mobile and in a web browser. Gemini 3.5 Flash-Lite was used in the Google Gemini app, in a browser, for the image-only run, and in Google AI Studio, in a browser, for the image + location run.

The Gemini app does not let the user disable web search. The image-only run there showed no web searches. In two attempts at the location run, however, the model searched the web despite being instructed not to; both attempts were discarded, and the run was repeated in AI Studio with web search disabled.

**Consequence for Gemini's paired comparison.** Because Gemini's two conditions were run in different interfaces, the difference between them combines the effect of the location with any effect of the interface (system instructions, image handling, default settings). These cannot be separated with this data, so Gemini's paired results should be read with more caution than those of the other six models.

**Medium reasoning effort** was used for each model. Each interface defines its effort levels differently, however, so differences in the actual amount of reasoning between models cannot be excluded and are likely. A model marketed with the same name through a future API or aggregator may expose different image preprocessing, token budgets, hidden instructions, tool access, and version snapshots.

| Replication-critical setting                   | Status                                                                                                                                      |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| User-facing model labels                       | Recorded above                                                                                                                              |
| Exact dated model build/version hashes         | **Not captured**                                                                                                                            |
| Reasoning/thinking budgets for each model      | Medium selected in each interface; the underlying budgets are not disclosed and may differ between providers                                |
| Image size, downsampling/compression on upload | **Not controlled across providers**                                                                                                         |
| Prompt texts                                   | Available verbatim in `PROMPTS.md`                                                                                                          |
| Image order                                    | 001–030, locked                                                                                                                             |
| Location labels                                | Verbatim, as sent, in `specimens_public.csv`                                                                                                |
| Tools/web access                               | Explicitly prohibited by prompt; web search disabled wherever the interface allowed it (not possible in the Gemini app; see above)          |
| Memory isolation                               | Cross-conversation retrieval discovered in excluded early runs; none observed in the scored runs, but this cannot be independently verified |
| Temperature, sampling seed, repeat trials      | **Not recorded/not controlled**                                                                                                             |

## Why this matters

Testing in the consumer apps was a **deliberate choice**: it is where most people actually ask a model to identify an animal, so the results describe what those users would receive. The trade-off is control. This benchmark measures these models **as accessed in these user-facing products and sessions**, not architecture-controlled, stateless versions of the model weights. Comparisons may reflect interface defaults, hidden system instructions and available context in addition to image understanding, and those factors can change over time without notice.

A future run through APIs could add control and exact reproducibility.
