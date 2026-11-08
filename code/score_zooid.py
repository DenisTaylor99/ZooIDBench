"""ZooIDBench scorer for two conditions (image only, image + location).

The answer key is read from data/specimens_public.csv: one row per image, with the
ground-truth species, the verified subspecies (or "none"), the taxonomic group and the
maximum score. Nothing about the specimens is written in this script, so the same
scorer can be used on another dataset by replacing that file and the response files.

What *is* written in this script is the pilot's adjudication layer (blind labels,
accepted synonyms, manual overrides and fabricated-name decisions), in the section
marked "Dataset-specific adjudications" below. Those are decisions about particular
answers; replace or empty them when scoring a different dataset.

Adjudication decisions were made by the experimenter with model identities hidden behind
letters A-G. Overrides are therefore keyed by (condition, blind label, image number). The
letter-to-model mapping differs between conditions and is defined in BLIND_LABELS.

Usage (from the repository root, Python 3 standard library only):
    python code/score_zooid.py
Optional: python code/score_zooid.py <repository root>

Inputs:  data/specimens_public.csv
         data/responses/image_only/<Model name>.md
         data/responses/image_plus_location/<Model name>_location.md
Outputs (written to data/; N is the number of models x the number of images):
         image_only_responses_scored_N.csv, location_responses_scored_N.csv
         image_only_summary.csv, location_summary.csv
         image_only_adjudications.csv, location_adjudications.csv
         paired_per_image.csv, paired_model_summary.csv
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
ANSWER_KEY = DATA / 'specimens_public.csv'

CONDITIONS = {
    'image_only': {'folder': 'image_only', 'suffix': '', 'prefix': 'image_only'},
    'image_plus_location': {'folder': 'image_plus_location', 'suffix': '_location', 'prefix': 'location'},
}

# Rubric (see docs/SCORING.md). A specimen's maximum is 3 if it has a verified subspecies, otherwise 2.
POINTS = {
    'wrong genus / non-answer': 0.0,
    'correct genus; incorrect species': 0.5,
    'genus only': 1.0,
    'correct species; wrong subspecies': 1.5,
    'correct species; no validated subspecies': 2.0,
    'correct subspecies': 3.0,
}
FABRICATION_PENALTY = 0.5

# ---------------------------------------------------------------------------
# Dataset-specific adjudications (ZooIDBench snake pilot, v0.1.0)
# ---------------------------------------------------------------------------

# Blind labels used during adjudication (reshuffled between conditions).
BLIND_LABELS = {
    'image_only': {'A': 'Claude Haiku 5.5', 'B': 'GPT-6 Astra', 'C': 'Gemini 3.5 Flash-Lite',
                   'D': 'Claude Sonnet 5.5', 'E': 'Claude Opus 5.5', 'F': 'GPT-6 Luna', 'G': 'GPT-6.1 Sol'},
    'image_plus_location': {'A': 'GPT-6 Luna', 'B': 'Gemini 3.5 Flash-Lite', 'C': 'GPT-6.1 Sol',
                            'D': 'Claude Haiku 5.5', 'E': 'Claude Opus 5.5', 'F': 'GPT-6 Astra',
                            'G': 'Claude Sonnet 5.5'},
}
# Order in which models appear in the summary files.
MODEL_ORDER = ['GPT-6 Astra', 'GPT-6.1 Sol', 'Claude Opus 5.5', 'Claude Sonnet 5.5',
               'GPT-6 Luna', 'Gemini 3.5 Flash-Lite', 'Claude Haiku 5.5']

# Historical names credited under the pilot's synonym policy (see docs/SCORING.md).
# An alias earns credit at species level only, never at subspecies level.
ALIASES = {'Morelia amethistina': 'Simalia amethistina', 'Boiga dendrophila': 'Boiga melanota',
           'Boiga dendrophila melanota': 'Boiga melanota', 'Azemiops kharini': 'Azemiops feae',
           'Bothrochilus albertisii': 'Leiopython albertisii', 'Maticora bivirgata': 'Calliophis bivirgatus'}

# Explanatory notes attached when a given image receives a given answer:
# (image number, 'prefix' or 'exact', answer, note).
ANSWER_NOTES = [
    (10, 'prefix', 'Boiga dendrophila',
     'Former broad taxonomy: Boiga dendrophila / B. d. melanota accepted for B. melanota at species level; no extra subspecies point'),
    (15, 'exact', 'Azemiops kharini', 'Azemiops kharini accepted as synonym under pilot policy'),
    (18, 'exact', 'Thelotornis capensis capensis', 'Species has no subspecies in locked dataset; max remains 2'),
]

# Manual adjudications: (condition, blind label, image) -> (adjudicated identification, reason).
# 'MULTIPLE_SPECIMENS' marks an answer describing more than one animal; it scores zero.
OVERRIDES = {
    ('image_only', 'A', 3): ('', 'Explicit non-answer ("I cannot place this specimen")'),
    ('image_only', 'A', 17): ('', 'Unresolved at genus level'),
    ('image_only', 'D', 2): ('Morelia spilota spilota', 'Subspecies explicitly identified in status field'),
    ('image_only', 'D', 3): ('Cerrophidion', 'Final restated identification after self-corrections'),
    ('image_plus_location', 'D', 6): ('MULTIPLE_SPECIMENS', 'Two fictitious snakes described; scored zero by experimenter decision'),
    ('image_plus_location', 'D', 12): ('MULTIPLE_SPECIMENS', 'Two fictitious snakes described; scored zero by experimenter decision'),
    ('image_plus_location', 'G', 2): ('Morelia spilota spilota', 'Explicit self-correction following initial cheynei identification'),
    ('image_plus_location', 'G', 8): ('Nerodia fasciata confluens', 'Explicit subspecies in identification despite genus-first wording'),
    ('image_plus_location', 'G', 15): ('Dinodon', 'Final genus-only answer; explicitly rejects earlier guessed species'),
    ('image_plus_location', 'G', 23): ('Candoia', 'Final self-correction to Candoia (final-answer rule)'),
    ('image_plus_location', 'G', 24): ('Leiopython', 'Genus only'),
    ('image_plus_location', 'G', 28): ('Eunectes notaeus', 'Best-supported species explicitly given, despite genus-first wording'),
    ('image_plus_location', 'D', 7): ('Naja', 'Two alternative species, no single species selected'),
    ('image_plus_location', 'D', 8): ('Nerodia', 'Genus-only response; species presented tentatively and status says species unidentified'),
    ('image_plus_location', 'D', 15): ('Sinomicrurus', 'Genus-only answer'),
    ('image_plus_location', 'D', 21): ('Pseudechis', 'Explicit genus; tentative species only, no supported species identification'),
}
# Notes that do not change the parsed identification.
EXTRA_NOTES = {
    ('image_plus_location', 'C', 23): 'Genus-only answer; previously mis-parsed as non-answer',
    ('image_plus_location', 'G', 15): 'Dinodon is a former genus name (now generally placed in Lycodon); wrong for this specimen either way',
    ('image_plus_location', 'B', 24): 'Bothrochilus albertisii is a documented synonym of Leiopython albertisii',
}
# Adjudicated fabricated names: combinations that never existed as valid or historical names.
FABRICATED = {
    ('image_only', 'G', 16): 'Zamenis leopardinus: unsupported combination (the historical name is Coluber leopardinus)',
    ('image_plus_location', 'B', 19): 'Simalia clarki: unsupported combination (the historical name is Liasis clarki)',
    ('image_plus_location', 'B', 25): 'Thamnophis sirtalis trifasciatus: no such recognized subspecies',
}

# ---------------------------------------------------------------------------
# Generic scoring code
# ---------------------------------------------------------------------------

CONF_RE = {k: re.compile(r'(?mi)^\s*-\s*' + k + r':\s*(Low-Medium|Medium-High|Low|Medium|High|N/A)\b')
           for k in ('Genus', 'Species', 'Subspecies')}
HEADING_RE = re.compile(r'(?m)^###\s+img_(\d+)\.([A-Za-z]+)[^\n]*\n')


def load_answer_key(path=ANSWER_KEY):
    """Read the answer key into {image number: specimen dict}, checking it against the rubric."""
    if not path.exists():
        raise SystemExit(f'Missing answer key: {path}')
    key = {}
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            m = re.match(r'^img_(\d+)\.', row['image'])
            if not m:
                raise SystemExit(f'Unexpected image name in answer key: {row["image"]}')
            i = int(m.group(1))
            if i in key:
                raise SystemExit(f'Duplicate image in answer key: {row["image"]}')
            species = row['ground_truth_species'].strip()
            sub = row['verified_subspecies'].strip()
            sub = '' if sub.lower() in ('', 'none') else sub
            if len(species.split()) != 2:
                raise SystemExit(f'{row["image"]}: ground_truth_species must be a binomial, got "{species}"')
            if sub and not sub.startswith(species + ' '):
                raise SystemExit(f'{row["image"]}: subspecies "{sub}" does not belong to species "{species}"')
            try:
                max_score = int(row['max_score'])
            except ValueError:
                raise SystemExit(f'{row["image"]}: max_score must be a whole number, got "{row["max_score"]}"')
            if max_score != (3 if sub else 2):
                raise SystemExit(f'{row["image"]}: max_score {row["max_score"]} contradicts the rubric '
                                 f'(3 with a verified subspecies, otherwise 2)')
            key[i] = dict(species=species, subspecies=sub, group=row.get('taxonomic_group', '').strip(),
                          max_score=max_score)
    return key


def response_path(condition, model):
    c = CONDITIONS[condition]
    path = DATA / 'responses' / c['folder'] / f"{model}{c['suffix']}.md"
    if not path.exists():
        raise SystemExit(f'Missing response file: {path}')
    return path


def parse_identification(line):
    """Leading binomial/trinomial of an identification line; 'Genus sp.' gives the genus only."""
    clean = re.sub(r'[_*]', '', line).strip()
    m = re.match(r'^([A-Z][a-z]+)(?:\s+|$)(?:\([A-Z][a-z]+\)\s+)?([a-z]+)?(?:\s+([a-z]+))?', clean)
    return ' '.join(z for z in m.groups() if z and z != 'sp') if m else ''


def answer_notes(i, predicted):
    notes = []
    for image, mode, name, note in ANSWER_NOTES:
        if i == image and (predicted.startswith(name) if mode == 'prefix' else predicted == name):
            notes.append(note)
    return notes


def score_condition(condition, key):
    rows = []
    n_images = len(key)
    for label, model in BLIND_LABELS[condition].items():
        raw = response_path(condition, model).read_text(encoding='utf-8')
        fragments = HEADING_RE.split(raw)
        assert len(fragments) == 1 + 3 * n_images, (condition, model, (len(fragments) - 1) // 3, 'sections found')
        seen = set()
        for idx_str, extension, block in zip(fragments[1::3], fragments[2::3], fragments[3::3]):
            i = int(idx_str)
            assert i in key, (condition, model, f'img_{i:03d} is not in the answer key')
            assert i not in seen, (condition, model, f'img_{i:03d} appears twice')
            seen.add(i)
            k = (condition, label, i)
            spec = key[i]

            idlines = re.findall(r'(?mi)^\s*(?:\*\*)?Identification(?:\*\*)?:\s*(.*?)\s*$', block)
            statuses = re.findall(r'(?mi)^\s*(?:\*\*)?Subspecies status(?:\*\*)?:\s*(.*?)\s*$', block)
            assert idlines, (condition, model, i, 'no Identification line')
            conf = {}
            for rank, rx in CONF_RE.items():
                m = rx.search(block)
                conf[rank] = m.group(1) if m else ''
            raw_id = ' | '.join(x.strip() for x in idlines)
            status = statuses[0].strip() if statuses else ''

            # Parse the first identification line; the raw text is kept for review.
            predicted = parse_identification(idlines[0])
            notes = []
            if k in EXTRA_NOTES:
                notes.append(EXTRA_NOTES[k])
            if k in OVERRIDES:
                predicted, why = OVERRIDES[k]
                notes.append(why)
            notes += answer_notes(i, predicted)

            species_gt, sub_gt = spec['species'], spec['subspecies']
            gt = sub_gt or species_gt
            genus_gt = species_gt.split()[0]
            alias = predicted in ALIASES
            canonical = ALIASES.get(predicted, predicted)
            pc = canonical.split()
            multi = predicted == 'MULTIPLE_SPECIMENS'
            pg = '' if multi else (pc[0] if pc else '')
            species_pred = '' if multi else (' '.join(pc[:2]) if len(pc) >= 2 else '')
            subspecies_pred = '' if multi else (' '.join(pc[:3]) if len(pc) >= 3 else '')
            genus_ok = pg == genus_gt
            species_attempted = len(pc) >= 2 and not multi
            species_ok = genus_ok and species_attempted and species_pred == species_gt
            subspecies_attempted = len(pc) >= 3 and not multi and not alias
            subspecies_ok = subspecies_attempted and bool(sub_gt) and subspecies_pred == sub_gt
            wrong_sub = species_ok and subspecies_attempted and not subspecies_ok and bool(sub_gt)
            fabricated = k in FABRICATED

            if not genus_ok:
                category = 'wrong genus / non-answer'
            elif not species_attempted:
                category = 'genus only'
            elif not species_ok:
                category = 'correct genus; incorrect species'
            elif subspecies_ok:
                category = 'correct subspecies'
            elif wrong_sub:
                category = 'correct species; wrong subspecies'
            else:
                category = 'correct species; no validated subspecies'
            points = POINTS[category]
            if fabricated:
                points = max(0.0, points - FABRICATION_PENALTY)
                notes.append(f'Fabricated name, -{FABRICATION_PENALTY} penalty: ' + FABRICATED[k])
            sensitivity = points + (0.5 if category in ('correct genus; incorrect species',
                                                        'correct species; wrong subspecies') else 0)
            if multi:
                notes.append('Score 0 by experimenter decision; not a fabricated name')

            low = status.lower()
            status_code = ('identified' if low.startswith('identified:') else
                           'recognized_not_identifiable' if low.startswith('recognized') else
                           'none_recognized' if low.startswith('no recognized') else
                           'undetermined' if low.startswith('undetermined') else 'other/missing')
            expected_status = ('identified' if subspecies_ok else
                               'recognized_not_identifiable' if sub_gt and species_ok else
                               'none_recognized' if species_ok else 'undetermined')
            rows.append(dict(
                model_name=model, blind_label=label, condition=condition, image=f'img_{i:03d}.{extension}',
                image_id=i, taxonomic_group=spec['group'], ground_truth=gt, ground_truth_species=species_gt,
                ground_truth_subspecies=sub_gt, possible_points=spec['max_score'],
                raw_identification=raw_id, raw_subspecies_status=status, raw_section=block.strip(),
                adjudicated_identification=predicted, normalized_identification=canonical, taxonomic_alias=int(alias),
                confidence_genus=conf['Genus'], confidence_species=conf['Species'], confidence_subspecies=conf['Subspecies'],
                genus_correct=int(genus_ok), species_attempted=int(species_attempted), species_correct=int(species_ok),
                subspecies_attempted=int(subspecies_attempted), subspecies_correct=int(subspecies_ok),
                subspecies_status_reported=status_code, subspecies_status_expected=expected_status,
                subspecies_status_correct_provisional=int(status_code == expected_status),
                scoring_category=category, fabricated_name=int(fabricated), false_multi_specimen=int(multi),
                score=points, score_no_specificity_penalty=sensitivity, adjudication_notes='; '.join(notes)))
        assert seen == set(key), (condition, model, 'missing images', sorted(set(key) - seen))

    # Validation invariants (see docs/REPRODUCIBILITY.md).
    n_models = len(BLIND_LABELS[condition])
    max_total = sum(s['max_score'] for s in key.values())
    assert len(rows) == n_models * n_images
    assert sum(r['possible_points'] for r in rows) == max_total * n_models
    assert all(0 <= r['score'] <= r['possible_points'] for r in rows)
    assert all(r['species_attempted'] or not r['species_correct'] for r in rows)
    assert all(r['species_correct'] or not r['subspecies_correct'] for r in rows)
    assert all(r['genus_correct'] or not r['species_correct'] for r in rows)
    return rows


def summarize(rows, key):
    n_images = len(key)
    max_total = sum(s['max_score'] for s in key.values())
    out = []
    for model in MODEL_ORDER:
        g = [r for r in rows if r['model_name'] == model]
        high = [r for r in g if r['confidence_species'] == 'High' and r['species_attempted']]
        pts = sum(r['score'] for r in g)
        att = sum(r['species_attempted'] for r in g)
        sp = sum(r['species_correct'] for r in g)
        out.append(dict(
            model_name=model, blind_label=g[0]['blind_label'], points=pts, max_points=max_total,
            normalized_percent=round(pts / max_total * 100, 2), genus_correct=sum(r['genus_correct'] for r in g),
            species_attempted=att, species_correct=sp, species_accuracy_percent=round(sp / n_images * 100, 2),
            species_selective_accuracy_percent=round(sp / att * 100, 2) if att else '',
            subspecies_correct=sum(r['subspecies_correct'] for r in g if r['ground_truth_subspecies']),
            subspecies_possible=sum(1 for r in g if r['ground_truth_subspecies']),
            high_confidence_attempted=len(high), high_confidence_correct=sum(r['species_correct'] for r in high),
            false_multi_specimen=sum(r['false_multi_specimen'] for r in g),
            fabricated_names=sum(r['fabricated_name'] for r in g),
            sensitivity_score=sum(r['score_no_specificity_penalty'] for r in g)))
    return out


def mcnemar_exact(k, n):
    """Two-sided exact McNemar test: binomial test on the discordant pairs."""
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(0, min(k, n - k) + 1)) / 2 ** n)


def write_csv(path, data):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, list(data[0]))
        w.writeheader()
        w.writerows(data)


def main():
    key = load_answer_key()
    images = sorted(key)
    n_images = len(images)
    max_total = sum(s['max_score'] for s in key.values())

    scored = {}
    for condition, c in CONDITIONS.items():
        rows = score_condition(condition, key)
        scored[condition] = {(r['model_name'], r['image_id']): r for r in rows}
        p = c['prefix']
        write_csv(DATA / f'{p}_responses_scored_{len(rows)}.csv', rows)
        write_csv(DATA / f'{p}_summary.csv', summarize(rows, key))
        cols = ['model_name', 'blind_label', 'image_id', 'ground_truth', 'raw_identification',
                'adjudicated_identification', 'normalized_identification', 'score', 'adjudication_notes']
        write_csv(DATA / f'{p}_adjudications.csv', [{k: r[k] for k in cols} for r in rows if r['adjudication_notes']])

    io, loc = scored['image_only'], scored['image_plus_location']
    pairs, summary = [], []
    for model in MODEL_ORDER:
        gained = lost = up = down = 0
        for i in images:
            a, z = io[(model, i)], loc[(model, i)]
            change = 'improved' if z['score'] > a['score'] else 'worsened' if z['score'] < a['score'] else 'unchanged'
            up += change == 'improved'
            down += change == 'worsened'
            gained += (not a['species_correct']) and z['species_correct']
            lost += a['species_correct'] and not z['species_correct']
            pairs.append(dict(model_name=model, image_id=i, ground_truth=a['ground_truth'],
                              image_only_identification=a['adjudicated_identification'], score_image_only=a['score'],
                              location_identification=z['adjudicated_identification'], score_location=z['score'],
                              change=change))
        si = sum(io[(model, i)]['score'] for i in images)
        sl = sum(loc[(model, i)]['score'] for i in images)
        spi = sum(io[(model, i)]['species_correct'] for i in images)
        spl = sum(loc[(model, i)]['species_correct'] for i in images)
        summary.append(dict(
            model_name=model, points_image_only=si, points_location=sl, max_points=max_total,
            normalized_percent_image_only=round(si / max_total * 100, 2),
            normalized_percent_location=round(sl / max_total * 100, 2),
            score_gain_pp=round((sl - si) / max_total * 100, 2),
            species_correct_image_only=spi, species_correct_location=spl,
            species_gain_pp=round((spl - spi) / n_images * 100, 2), images_improved=up,
            images_unchanged=n_images - up - down, images_worsened=down, species_gained=gained, species_lost=lost,
            mcnemar_exact_p_species=round(mcnemar_exact(lost, gained + lost), 4)))
    write_csv(DATA / 'paired_per_image.csv', pairs)
    write_csv(DATA / 'paired_model_summary.csv', summary)

    for s in summary:
        print(s)


if __name__ == '__main__':
    main()
