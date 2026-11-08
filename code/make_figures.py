"""ZooIDBench figures, drawn from the CSVs written by code/score_zooid.py.

Run the scorer first, then, from the repository root:
    python code/make_figures.py
Optional: python code/make_figures.py <repository root>

Requires matplotlib (pip install matplotlib). Everything plotted is read from data/:
the models and their order, the maximum score, the number of images and the taxonomic
groups. Nothing about the results is written in this script, so after re-scoring (or
scoring a new dataset) running it again redraws the figures with the new numbers.
Only the wording below (titles and footnotes) is specific to this pilot.

Outputs (written to figures/):
    01_normalized_score.png                   normalized score, both conditions
    02_species_named_correct.png              species named vs species correct
    03_high_confidence.png                    High-confidence species answers vs correct
    04_heatmap.png                            score by taxonomic group
"""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
OUT = ROOT / 'figures'

# ---------------------------------------------------------------------------
# Wording specific to this pilot: edit freely. {n_images}, {max_points} and
# {n_models} are filled in from the data.
# ---------------------------------------------------------------------------
SUBJECT = 'snake photographs'
NOTE_OVERALL = ("Normalized score = points / {max_points} × 100. Gemini 3.5 Flash-Lite's two conditions "
                "were run in different interfaces (Gemini app, Google AI Studio).")
CONDITION_LABELS = {'io': 'Image only', 'loc': 'Image + location'}
# Column order of the heatmap. Groups found in the data but not listed here are added at the end.
GROUP_ORDER = ['Colubrids', 'Vipers', 'Elapids', 'Pythons', 'Boas']

# ---------------------------------------------------------------------------
# Style (validated colour-blind-safe pair; lighter tints of the same hues).
# ---------------------------------------------------------------------------
SURF, INK, INK2, MUTED, GRID, RULE = '#ffffff', '#0b0b0b', '#52514e', '#8a8984', '#ebeae6', '#c9c8c2'
COLOR = {'io': '#2a78d6', 'loc': '#eb6834'}
TINT = {'io': '#b7d3f6', 'loc': '#f8c7b0'}
HEAT = ['#f3f8fe', '#cde2fb', '#86b6ef', '#3987e5', '#256abf', '#104281']
DPI = 200


def setup_fonts():
    """Use Inter if it is installed; otherwise matplotlib's default font."""
    for f in font_manager.findSystemFonts():
        if 'inter' in Path(f).name.lower():
            try:
                font_manager.fontManager.addfont(f)
            except Exception:
                pass
    names = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({'font.family': 'Inter' if 'Inter' in names else 'sans-serif', 'font.size': 10,
                         'axes.edgecolor': RULE, 'axes.labelcolor': INK2,
                         'xtick.color': INK2, 'ytick.color': INK})


def read(name):
    path = DATA / name
    if not path.exists():
        raise SystemExit(f'Missing {path}: run code/score_zooid.py first.')
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def scored_file(prefix):
    files = sorted(DATA.glob(f'{prefix}_responses_scored_*.csv'))
    if len(files) != 1:
        raise SystemExit(f'Expected one data/{prefix}_responses_scored_N.csv, found {len(files)}.')
    return files[0].name


def header(fig, title, subtitle):
    fig.text(0.012, 0.975, title, fontsize=14, fontweight='semibold', color=INK, va='top')
    fig.text(0.012, 0.925, subtitle, fontsize=10.5, color=INK2, va='top')


def footnote(fig, text):
    fig.text(0.012, 0.02, text, fontsize=8.5, color=MUTED, va='bottom')


def style_axis(ax, xlabel):
    ax.set_xlabel(xlabel, fontsize=9.5)
    ax.grid(axis='x', color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0, labelsize=10.5)
    ax.tick_params(axis='x', labelsize=9)


def nice_step(n):
    return next(s for s in (1, 2, 5, 10, 20, 25, 50, 100) if n / s <= 7)


def chart_overall(paired, models, max_points, n_images):
    fig, ax = plt.subplots(figsize=(10, 1.6 + 0.5 * len(models)), facecolor=SURF)
    fig.subplots_adjust(left=0.2, right=0.97, top=1 - 1.25 / fig.get_figheight(),
                        bottom=0.85 / fig.get_figheight())
    ys = list(range(len(models)))[::-1]
    for y, r in zip(ys, paired):
        a = float(r['points_image_only']) / max_points * 100
        b = float(r['points_location']) / max_points * 100
        ax.plot([a, b], [y, y], color='#d6d5cf', lw=3, solid_capstyle='round', zorder=1)
        left, right = (a, b) if a <= b else (b, a)
        ax.scatter([a], [y], s=110, color=COLOR['io'], edgecolor=SURF, linewidth=2, zorder=3)
        ax.scatter([b], [y], s=110, color=COLOR['loc'], edgecolor=SURF, linewidth=2, zorder=3)
        ax.text(left - 2.2, y, f'{left:.1f}%', ha='right', va='center', fontsize=9.5,
                color=INK2 if left == a else INK, fontweight='normal' if left == a else 'semibold')
        ax.text(right + 2.2, y, f'{right:.1f}%', ha='left', va='center', fontsize=9.5,
                color=INK if right == b else INK2, fontweight='semibold' if right == b else 'normal')
        ax.text(108, y, f'{b - a:+.1f} pp', ha='left', va='center', fontsize=9, color=MUTED)
    ax.text(108, len(models) - 0.35, 'Change', fontsize=9, color=MUTED, ha='left')
    ax.set_yticks(ys, models)
    style_axis(ax, f'Normalized score (% of {max_points:g} possible points)')
    ax.set_xlim(0, 118)
    ax.set_xticks(range(0, 101, 20))
    ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=9, color=COLOR[c], label=CONDITION_LABELS[c])
                       for c in ('io', 'loc')],
              loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=10,
              handletextpad=0.3, borderaxespad=0.2)
    header(fig, 'Normalized score with and without location',
           f'{len(models)} models, {n_images} {SUBJECT}; models ordered by score with location')
    footnote(fig, NOTE_OVERALL.format(max_points=f'{max_points:g}', n_images=n_images, n_models=len(models)))
    fig.savefig(OUT / '01_normalized_score.png', dpi=DPI, facecolor=SURF)
    plt.close(fig)


def chart_part_of_whole(summ, models, n_images, fname, title, subtitle, whole_key, part_key,
                        part_name, rest_name, note, empty_text):
    fig, axes = plt.subplots(1, 2, figsize=(11, 2.0 + 0.55 * len(models)), sharey=True, facecolor=SURF)
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.17, right=0.98, top=1 - 1.4 / h, bottom=1.3 / h, wspace=0.08)
    ys = list(range(len(models)))[::-1]
    for ax, cond in zip(axes, ('io', 'loc')):
        for y, m in zip(ys, models):
            whole, part = int(summ[cond][m][whole_key]), int(summ[cond][m][part_key])
            if whole == 0:
                ax.text(0.4, y, empty_text, va='center', ha='left', fontsize=9, color=MUTED, style='italic')
                continue
            ax.barh(y, whole, height=0.62, color=TINT[cond], linewidth=0)
            ax.barh(y, part, height=0.62, color=COLOR[cond], linewidth=0)
            ax.text(whole + n_images * 0.013, y, f'{part} / {whole}', va='center', ha='left', fontsize=9.5, color=INK)
        ax.axvline(n_images, color=RULE, lw=1, ls=(0, (2, 2)))
        style_axis(ax, f'Photographs (out of {n_images})')
        ax.set_xlim(0, n_images * 1.15)
        ax.set_xticks(range(0, n_images + 1, nice_step(n_images)))
        ax.set_title(CONDITION_LABELS[cond], loc='left', fontsize=11.5, fontweight='semibold',
                     color=COLOR[cond], pad=8)
        ax.legend(handles=[Patch(color=COLOR[cond], label=part_name), Patch(color=TINT[cond], label=rest_name)],
                  loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False, fontsize=9)
    axes[0].set_yticks(ys, models)
    header(fig, title, subtitle)
    footnote(fig, note)
    fig.savefig(OUT / fname, dpi=DPI, facecolor=SURF)
    plt.close(fig)


def chart_heatmap(scored, models):
    groups, gmax = [], {}
    first = models[0]
    for r in scored['io']:
        g = r['taxonomic_group'] or 'Ungrouped'
        if g not in groups:
            groups.append(g)
        if r['model_name'] == first:
            gmax[g] = gmax.get(g, 0) + float(r['possible_points'])
    groups = [g for g in GROUP_ORDER if g in groups] + [g for g in groups if g not in GROUP_ORDER]
    sizes = {}
    for r in scored['io']:
        if r['model_name'] == first:
            g = r['taxonomic_group'] or 'Ungrouped'
            sizes[g] = sizes.get(g, 0) + 1
    cmap = LinearSegmentedColormap.from_list('seq', HEAT)
    fig, axes = plt.subplots(1, 2, figsize=(4.5 + 1.4 * len(groups), 1.6 + 0.6 * len(models)),
                             sharey=True, facecolor=SURF)
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.17, right=0.9, top=1 - 1.3 / h, bottom=0.65 / h, wspace=0.05)
    im = None
    for ax, cond in zip(axes, ('io', 'loc')):
        pts = {(m, g): 0.0 for m in models for g in groups}
        for r in scored[cond]:
            pts[(r['model_name'], r['taxonomic_group'] or 'Ungrouped')] += float(r['score'])
        grid = [[pts[(m, g)] / gmax[g] * 100 for g in groups] for m in models]
        im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=100, aspect='auto')
        for i, m in enumerate(models):
            for j, g in enumerate(groups):
                v = grid[i][j]
                dark = v >= 55
                ax.text(j, i - 0.12, f'{v:.0f}%', ha='center', va='center', fontsize=10,
                        color='#ffffff' if dark else INK, fontweight='semibold')
                ax.text(j, i + 0.24, f'{pts[(m, g)]:g}/{gmax[g]:g}', ha='center', va='center', fontsize=7.5,
                        color='#ffffff' if dark else INK2)
        ax.set_xticks(range(len(groups)), [f'{g}\n/{gmax[g]:g}' for g in groups], fontsize=9.5)
        ax.xaxis.tick_top()
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xticks([x - 0.5 for x in range(1, len(groups))], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, len(models))], minor=True)
        ax.grid(which='minor', color=SURF, lw=2)
        ax.tick_params(which='minor', length=0)
        ax.set_xlabel(CONDITION_LABELS[cond], fontsize=11.5, fontweight='semibold', color=COLOR[cond], labelpad=8)
    axes[0].set_yticks(range(len(models)), models, fontsize=10.5)
    cax = fig.add_axes([0.915, 0.65 / h, 0.015, 1 - 1.95 / h])
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_label("% of the group's possible points", color=INK2, fontsize=9)
    cb.ax.tick_params(labelsize=8.5, length=0)
    lo, hi = min(sizes.values()), max(sizes.values())
    span = f'{lo}' if lo == hi else f'{lo}–{hi}'
    header(fig, 'Score by taxonomic group',
           "Each cell: share of the group's possible points (large) and points / maximum (small). "
           f'Groups have {span} photographs, so single answers move cells a lot.')
    fig.savefig(OUT / '04_heatmap.png', dpi=DPI, facecolor=SURF)
    plt.close(fig)


def main():
    setup_fonts()
    OUT.mkdir(exist_ok=True)
    paired = read('paired_model_summary.csv')
    models = [r['model_name'] for r in paired]
    max_points = float(paired[0]['max_points'])
    summ = {'io': {r['model_name']: r for r in read('image_only_summary.csv')},
            'loc': {r['model_name']: r for r in read('location_summary.csv')}}
    scored = {'io': read(scored_file('image_only')), 'loc': read(scored_file('location'))}
    n_images = len({r['image_id'] for r in scored['io']})

    # Order models by score with location, highest first.
    paired.sort(key=lambda r: -float(r['points_location']))
    models = [r['model_name'] for r in paired]

    chart_overall(paired, models, max_points, n_images)
    chart_part_of_whole(
        summ, models, n_images, '02_species_named_correct.png',
        'Species named and species correct',
        'Full bar: photographs where the model named a species. Dark part: the species was correct.',
        'species_attempted', 'species_correct', 'Species correct', 'Species named, wrong',
        'Labels read correct / named. A model that names a species less often has fewer chances to be wrong, '
        'so compare both lengths.', 'none')
    chart_part_of_whole(
        summ, models, n_images, '03_high_confidence.png',
        'Species answers rated High confidence, and how many were right',
        'Full bar: species answers the model rated High confidence. Dark part: those that were correct.',
        'high_confidence_attempted', 'high_confidence_correct', 'High confidence, correct',
        'High confidence, wrong',
        'Confidence is self-reported on a five-level scale. "N/A": the model gave no species answer rated High.',
        'N/A, no High-confidence species answers')
    chart_heatmap(scored, models)
    print(f'Wrote 4 figures to {OUT}')


if __name__ == '__main__':
    main()
