# ESM-2 Viral Evolution — ICLR 2026 Course Report

**Title:** Frozen Protein Language Models Encode Viral Evolutionary Geometry Across Two Scales

**Author:** James Huang (University of Minnesota, Twin Cities)

This repository hosts the ICLR 2026 course final report and the figure-generation script for the surveillance methodology flowchart. The companion training/analysis codebase lives in [`huan2701-cmd/esm-tax`](https://github.com/huan2701-cmd/esm-tax).

## Layout

```
paper/iclr2026/
├── esm_viral_evolution.tex         # Main paper source
├── esm_viral_evolution.pdf         # Compiled output (9 pages)
├── esm_viral_refs.bib              # References
├── iclr2026_conference.{sty,bst}   # ICLR template (do not edit)
├── math_commands.tex               # Math macros
└── figures/
    ├── fig_pipeline_supervised.png        # Supervised 3-stage pipeline
    ├── fig_methodology_unsupervised.png   # Unsupervised flowchart (big-font)
    ├── fig_tsne_ranks.png                 # Per-rank t-SNE
    ├── fig_mutation_decomp.png            # Mutation-identity vs Hamming R²
    ├── fig_layerwise_lda.png              # Layer-wise LDA probe
    ├── fig_layerwise_mut.png
    ├── fig_domain_validation.png          # Domain enrichment
    ├── fig_3d_mapping.png                 # PDB 3D residue mapping
    └── fig_baseline_pca.png               # Alignment baseline

scripts/
└── draw_methodology_flowchart.py   # Regenerates fig_methodology_unsupervised.png
```

## Build

```bash
cd paper/iclr2026
pdflatex esm_viral_evolution.tex
bibtex   esm_viral_evolution
pdflatex esm_viral_evolution.tex
pdflatex esm_viral_evolution.tex
```

Requires a working TeX distribution (TinyTeX / TeX Live / MiKTeX).

## Regenerate the unsupervised flowchart

```bash
pip install matplotlib numpy
python scripts/draw_methodology_flowchart.py
```

Output: `results/surveillance/sars_viz/fig_methodology_flowchart.png`. Copy it to `paper/iclr2026/figures/fig_methodology_unsupervised.png` before recompiling the paper.

## Notes

- `\iclrfinalcopy` is enabled in the preamble per the instructor's requirement.
- Fonts and spacing follow the ICLR template — do not modify.
- AI assistance disclosure: Claude (Anthropic) assisted with code, analysis scripting, and report writing; all experimental design, data interpretation, and scientific conclusions are the author's.
