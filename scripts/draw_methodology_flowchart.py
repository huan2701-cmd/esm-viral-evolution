from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(18, 26))
ax.set_xlim(0, 14)
ax.set_ylim(0, 22)
ax.axis('off')


def draw_box(ax, x, y, w, h, text, color, text_color='#1a1a1a', fontsize=14, bold=False):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.3",
                         facecolor=color, edgecolor='#333', linewidth=1.8, zorder=2)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, weight=weight, zorder=3,
            multialignment='center')


def draw_arrow(ax, x1, y1, x2, y2, color='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.2))


# ── Shared ESM-2 backbone banner ──────────────────────────────────────────
draw_box(ax, 1.5, 20.5, 11, 0.8,
         'Shared Frozen Backbone:  ESM-2 t33_650M  (frozen, fp16)  ·  1280-dim residue representations',
         '#e8eaf6', '#283593', fontsize=14, bold=True)
ax.annotate('', xy=(3.5, 20.5), xytext=(3.5, 20.2),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
ax.annotate('', xy=(10.5, 20.5), xytext=(10.5, 20.2),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))

# ── Title ─────────────────────────────────────────────────────────────────
ax.text(7, 21.4, 'ESM-2 Viral Variant Surveillance — Methodology',
        ha='center', va='center', fontsize=22, weight='bold', color='#1a1a2e')
ax.text(7, 20.95, 'From sequence embeddings to recombinant detection  ·  intra-species (bottom-up)',
        ha='center', va='center', fontsize=14, color='#555', style='italic')

# ── Column labels ─────────────────────────────────────────────────────────
ax.text(3.5, 19.95, 'Phase A: Space Exploration', ha='center', va='center',
        fontsize=16, weight='bold', color='#0f3460')
ax.text(10.5, 19.95, 'Phase B: Automated Surveillance', ha='center', va='center',
        fontsize=16, weight='bold', color='#b71c1c')

# ── LEFT COLUMN: Phase A ──────────────────────────────────────────────────
draw_box(ax, 1.5, 18.7, 4, 0.9,
         '804 SARS-CoV-2 Spike sequences\n(GISAID / GenBank)',
         '#e3f2fd', fontsize=13)
draw_arrow(ax, 3.5, 18.7, 3.5, 18.1)

draw_box(ax, 1.5, 17.1, 4, 0.9,
         'ESM-2 embeddings\n1280-dim protein language space',
         '#bbdefb', fontsize=14, bold=True)
draw_arrow(ax, 3.5, 17.1, 3.5, 16.5)

draw_box(ax, 1.5, 15.4, 4, 1.05,
         'Space probing\nPCA / UMAP / PHATE\nkNN local purity + entropy + neighbour enrichment OR',
         '#c8e6c9', fontsize=12)
draw_arrow(ax, 3.5, 15.4, 3.5, 14.8)

draw_box(ax, 1.0, 13.8, 5, 0.85,
         'Finding: signal not in max-variance direction\nPC1 = divergence axis (r = 0.958)',
         '#fff9c4', fontsize=13)
draw_arrow(ax, 3.5, 13.8, 3.5, 13.2)

draw_box(ax, 1.5, 12.1, 4, 1.05,
         'LDA finds discriminative directions\nLinear probe: 96.4% accuracy\nPC4 = lineage axis (F = 532)',
         '#a5d6a7', fontsize=12, bold=True)
draw_arrow(ax, 3.5, 12.1, 3.5, 11.5)

draw_box(ax, 1.5, 10.4, 4, 1.05,
         'Mutation decomposition\nHamming R²=0.003 → Identity R²=0.852\n280× lift  |  Top driver: L452R (Delta)',
         '#81c784', fontsize=12, bold=True)
draw_arrow(ax, 3.5, 10.4, 3.5, 9.8)

draw_box(ax, 1.5, 9.0, 4, 0.85,
         'Cross-virus validation\nRSV R²=0.853  |  Dengue R²=0.704',
         '#a5d6a7', fontsize=13)
draw_arrow(ax, 3.5, 9.0, 3.5, 8.4)

draw_box(ax, 1.5, 7.5, 4, 0.85,
         'Structural validation\nFisher OR=13.25 (p<0.0001)\n9/20 residues on known epitopes',
         '#66bb6a', fontsize=12, bold=True)

# ── RIGHT COLUMN: Phase B ─────────────────────────────────────────────────
draw_box(ax, 8.5, 18.7, 4, 0.9,
         'Global alignment preprocessing\nWuhan-Hu-1 as reference\nRemove 98% spurious mutations',
         '#ffebee', fontsize=12)
draw_arrow(ax, 10.5, 18.7, 10.5, 18.1)

draw_box(ax, 8.5, 17.1, 4, 0.9,
         'Mutation matrix → truncated SVD\n16-dim latent mutation space',
         '#ffcdd2', fontsize=14, bold=True)
draw_arrow(ax, 10.5, 17.1, 10.5, 16.5)

draw_box(ax, 8.5, 15.4, 4, 1.05,
         'kNN graph → graph clustering\nLouvain / HDBSCAN / GMM-BIC\nBootstrap stability (20×)',
         '#ef9a9a', fontsize=12)
draw_arrow(ax, 10.5, 15.4, 10.5, 14.8)

draw_box(ax, 8.0, 13.8, 5, 0.85,
         'SVD-HDBSCAN wins\nsil=0.895  |  ARI=0.992  |  pur=0.900',
         '#ffccbc', fontsize=13, bold=True)
draw_arrow(ax, 10.5, 13.8, 10.5, 13.2)

draw_box(ax, 8.5, 11.7, 4, 1.45,
         'Noise point analysis\n240/804 (29.9%) flagged as noise\nMutation profiles reveal\nmulti-VOC signature combinations',
         '#e57373', fontsize=12, bold=True)
draw_arrow(ax, 10.5, 11.7, 10.5, 11.1)

draw_box(ax, 8.0, 9.1, 5, 1.95,
         'Surveillance signals detected\n'
         '▸ BA.2/5+: 52% noise rate\n'
         '  del_69-70(α)+L452R(δ)+F486V(BA.4/5)\n'
         '▸ Delta: 25% lack G142D (Omicron)\n'
         '  → Delta-Omicron transition/recomb.\n'
         '▸ Other/Recomb: linear probe only 79%\n'
         '  mosaic structure; algorithm flags honestly',
         '#c62828', 'white', fontsize=11, bold=True)

# ── Bridge arrow ──────────────────────────────────────────────────────────
ax.annotate('', xy=(8.3, 17.3), xytext=(5.7, 17.3),
            arrowprops=dict(arrowstyle='<->', color='#666', lw=1.8, ls='--'))
ax.text(7.0, 17.6, 'ESM space signal\nguides feature engineering',
        ha='center', va='bottom', fontsize=12, color='#555', style='italic')

# ── Core conclusions ──────────────────────────────────────────────────────
ax.text(7, 6.8, 'Core Conclusions', ha='center', va='center',
        fontsize=18, weight='bold', color='#1a1a2e')

draw_box(ax, 0.7, 4.8, 12.6, 1.9,
         '1.  ESM-2 embeddings carry decodable lineage signal (96.4%), hidden in directions PCA misses\n'
         '2.  ESM-2 is sensitive to mutation identity, not just count  (280× over Hamming); generalises cross-virus\n'
         '3.  Unsupervised SVD-HDBSCAN auto-discovers clusters + noise;  noise = recombinants/transitions, no K needed\n'
         '4.  Algorithm captured 52% hidden recombinant signal in BA.2/5+, exposing label over-coarsening',
         '#e8f5e9', '#1b5e20', fontsize=12)

ax.text(7, 4.35,
        'Data: GISAID / GenBank  ·  Tools: fair-esm, scikit-learn, HDBSCAN, Biopython  ·  Structures: PDB 6VXX, 5WN9, 1OAN',
        ha='center', va='center', fontsize=11, color='#888')

plt.tight_layout()
out = 'results/surveillance/sars_viz/fig_methodology_flowchart.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f'[OK] Saved {out}')
