"""Build a bilingual (Chinese narrative + English captions) self-contained HTML
story for the TA. Images are base64-embedded so the file is fully portable.

Output: ../story_for_TA.html
"""
from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "paper" / "iclr2026" / "figures"
OUT = ROOT / "story_for_TA.html"


def img(name: str, alt: str, width: str = "82%") -> str:
    p = FIG_DIR / name
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return (
        f'<img src="data:image/png;base64,{b64}" alt="{alt}" '
        f'style="width:{width};max-width:100%;display:block;margin:14px auto;'
        f'border:1px solid #e0e0e0;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.06);" />'
    )


# ─── Sections ────────────────────────────────────────────────────────────────
SECTIONS: list[dict] = [
    {
        "n": 0,
        "zh_title": "一句话总结",
        "en_title": "TL;DR",
        "zh": (
            "用<b>冻结的 ESM-2 蛋白语言模型</b>，不做任何训练就能同时支持"
            "<b>跨物种病毒分类</b>（Kingdom→Order，90.6% 准确）和"
            "<b>种内变异监测</b>（SARS-CoV-2 VOC 聚类，silhouette 0.895，没用任何标签）。"
            "核心发现：进化几何已经在 ESM-2 的表征空间里了，不是微调出来的。"
        ),
        "en": (
            "A frozen protein language model (ESM-2) simultaneously enables hierarchical "
            "viral taxonomy (90.6% Order accuracy) AND unsupervised SARS-CoV-2 variant "
            "surveillance (silhouette 0.895) — without any task-specific training. "
            "Evolutionary geometry is intrinsic to the representation space."
        ),
        "img": None,
    },
    {
        "n": 1,
        "zh_title": "我去年踩过的坑：序列比对 + 随机森林",
        "en_title": "Last year's attempt: alignment + random forest",
        "zh": (
            "去年我做过一个类似的工作 —— 把 8 种病毒序列做 alignment，"
            "然后用随机森林画出一张「病毒地图」。当时跑完图就开始怀疑：<br><br>"
            "<b>这种纯序列相似度聚出来的图，真的有参考性吗？</b><br><br>"
            "答案是没有。它既看不出哪个病毒「特别」，也回答不了任何生物学问题，"
            "只是把序列上长得像的东西堆在一起。下面这张就是典型的"
            "alignment + PCA + K-means baseline —— 视觉上看着干净，"
            "是因为 MSA 已经把序列硬掰进了一个欧氏空间，"
            "对真正新出现的、高变异的病毒完全没用。"
        ),
        "en": (
            "Alignment-based clustering looks clean only because MSA forces sequences "
            "into a Euclidean-compatible subspace. It cannot answer biological questions "
            "and breaks on novel / highly divergent sequences."
        ),
        "img": ("fig_baseline_pca.png", "Alignment + PCA + K-means baseline"),
    },
    {
        "n": 2,
        "zh_title": "核心疑问：能不能用大语言模型替代？",
        "en_title": "Core question: can a PLM replace alignment?",
        "zh": (
            "技术都这么成熟了，能不能用<b>大语言模型</b>学到病毒进化的几何，"
            "或者起码做一个<b>快速检测</b>？<br><br>"
            "想象一下回到 2019 年武汉 —— 如果当时我们能在几分钟内：<br>"
            "&nbsp;&nbsp;① 把一段新序列定位到病毒大类，<br>"
            "&nbsp;&nbsp;② 找到与它最近的已知抗原，<br>"
            "会不会少死很多人？<br><br>"
            "这是我做这个项目的动机。"
        ),
        "en": (
            "Could a pretrained protein language model give us, in minutes, "
            "(1) taxonomic placement of a new virus and (2) its nearest known antigen? "
            "Imagine Wuhan 2019 with that capability."
        ),
        "img": None,
    },
    {
        "n": 3,
        "zh_title": "要回答的两个问题",
        "en_title": "Two concrete questions",
        "zh": (
            "<b>问题 1（跨物种）：</b>能不能用 ESM-2 embedding 快速区分病毒？"
            "对应分类任务。<br><br>"
            "<b>问题 2（种内）：</b>这套方法能不能接到现有工具链上？"
            "比如告诉我「这个新毒株最像 BA.5」、「它跟 Delta 共享了 L452R」？"
            "对应监测任务。<br><br>"
            "两个问题、一个模型 —— 这本身就是实验设计："
            "如果同一个冻结 backbone 能同时回答这两个尺度的问题，"
            "那进化几何就不是某个微调任务的副产品。"
        ),
        "en": (
            "Q1 (cross-species): can ESM-2 separate distinct viruses? "
            "Q2 (intra-species): can it support a surveillance toolchain — "
            "nearest-antigen retrieval, mutation co-occurrence reading? "
            "Same frozen backbone for both → tests whether the signal is intrinsic."
        ),
        "img": None,
    },
    {
        "n": 4,
        "zh_title": "为什么选 ESM-2 而不是 EVO2",
        "en_title": "Why ESM-2, not EVO2",
        "zh": (
            "心里的最优选其实是 <b>EVO2</b>（核酸级别的大模型），"
            "但是它的部署环境过于复杂，对单卡也不友好。<br><br>"
            "<b>ESM-2 蛋白→蛋白</b>这条路线反而更容易区分病毒，"
            "因为蛋白序列已经过了一层「自然选择压缩」，"
            "结构信号更显式。所以我从 6 帧翻译拿出 Pfam domain，"
            "送 ESM-2 跑 embedding。"
        ),
        "en": (
            "EVO2 was the ideal pretrained model but its deployment footprint is heavy. "
            "ESM-2 (protein-to-protein) gives sharper inter-virus separation because protein "
            "sequences are already compressed by natural selection. Pipeline: 6-frame "
            "translation → Pfam → frozen ESM-2 embedding."
        ),
        "img": None,
    },
    {
        "n": 5,
        "zh_title": "数据：公开、最小、Spike 一段就够",
        "en_title": "Data: public, minimal, Spike only",
        "zh": (
            "数据全是公开的（GISAID / GenBank / ICTV VMR），"
            "种内监测我甚至只摘了 SARS-CoV-2 的 <b>Spike</b> 一段、804 条序列。"
            "<br><br>流程极简：<b>序列 → ESM-2 → embedding</b>，就这样。"
        ),
        "en": (
            "All public data. For surveillance we use only the SARS-CoV-2 Spike (n=804). "
            "Pipeline is literally: sequence → ESM-2 → embedding."
        ),
        "img": None,
    },
    {
        "n": 6,
        "zh_title": "Embedding 被神化了？PCA 直接降维：乱成一团",
        "en_title": "PCA on raw embeddings: nothing",
        "zh": (
            "现在的风气是把 embedding 当万能钥匙。我就直接 PCA 给它降到 2D —— <br>"
            "结果 PC1 / PC2 几乎啥都没有，根本不是肉眼可见的 cluster。<br><br>"
            "换句话说，<b>「最大方差方向」并不是「最有信息的方向」</b>。"
            "这个发现后面会被反复验证。"
        ),
        "en": (
            "Top-2 PCA components on raw ESM-2 embeddings show no clean cluster structure. "
            "Maximum-variance directions ≠ most informative directions."
        ),
        "img": None,
    },
    {
        "n": 7,
        "zh_title": "「作弊」一下：用 LDA 看簇藏在哪里",
        "en_title": "Cheating with LDA to locate the signal",
        "zh": (
            "既然肉眼找不到，我就「作弊」 —— 用 <b>LDA</b>（监督的判别分析）"
            "直接问：簇在哪？<br><br>"
            "结论很有意思：从 PCA 角度看，可分簇信息<b>不在 PC1/PC2，"
            "而是大概落在 PC4 到 PC8</b> 这个区间。"
            "并且这个信号<b>从 Layer 1 就出现了</b>，不是深层涌现，"
            "而是预训练表征里本就埋着的。"
        ),
        "en": (
            "LDA reveals that the discriminative signal lives between PC4–PC8, "
            "not PC1–PC2. Layer-1 LDA already hits ~95% accuracy — this is not "
            "deep emergence, it is pretraining-encoded geometry."
        ),
        "img": ("fig_layerwise_lda.png", "Layer-wise LDA probe accuracy"),
    },
    {
        "n": 8,
        "zh_title": "随手记的小疑问：一定要标签才能做这些吗？",
        "en_title": "Side note: do we really need labels?",
        "zh": (
            "我记到随身的纸条上：<i>「一定要标签他才能做出这么好的东西吗？"
            "前人做 ESM-2 都是有监督的，我能不能不用标签也跑出来？」</i><br><br>"
            "这是<b>支线疑问</b>，不是主线 —— 主线是先把无监督方法跑通。"
            "（后面会回来跨物种线上做有监督，这就是另一个故事了。）"
        ),
        "en": (
            "Note to self: most prior ESM-2 works use supervision. Can we get away "
            "without labels? Filed as a side thread; the main line is unsupervised first."
        ),
        "img": None,
    },
    {
        "n": 9,
        "zh_title": "主线：把所有无监督方法都试一遍",
        "en_title": "Main line: exhaust unsupervised methods",
        "zh": (
            "于是我把无监督方法<b>挨个跑了一遍</b>：直接 K-means、HDBSCAN、"
            "autoencoder + GMM、kNN + Louvain、自学聚类的深度网络……<br><br>"
            "<b>最后赢的是 SVD-HDBSCAN</b>：先截断 SVD 去掉那些「最大方差但没信息」"
            "的 nuisance 维度（验证了第 6 节的猜测），再用 HDBSCAN 的密度聚类。"
            "结果是 silhouette = 0.895，ARI = 0.992，没有用任何 lineage 标签。<br><br>"
            "更有意思的是 —— <b>HDBSCAN 标为「噪声」的那 30% 点</b>，"
            "里面 BA.2/5+ 占了 52%。这些不是失败，这些是<b>重组体信号</b>："
            "del69-70 (Alpha) + L452R (Delta) + F486V (BA.4/5) 同时出现。"
            "Pango 给的「BA.2/5+」其实把至少 3 个独立的重组历史揉成了一个标签。"
        ),
        "en": (
            "Tried every unsupervised method on the menu. Winner: SVD-HDBSCAN "
            "(silhouette 0.895, ARI 0.992, no lineage labels). "
            "What looks like 30% 'noise' is actually recombinant signal — "
            "BA.2/5+ alone has a 52% noise rate driven by mosaic mutation combinations."
        ),
        "img": ("fig_methodology_unsupervised.png",
                 "Unsupervised surveillance methodology"),
    },
    {
        "n": 10,
        "zh_title": "回到支线：界门纲目，能不能粗犷地分准？",
        "en_title": "Back to the side thread: hierarchical classification",
        "zh": (
            "无监督跑完后，我回到那张纸条上的疑问。<br><br>"
            "高中学过<b>「界门纲目科属种」</b> —— 我就拿这个层级跑模型："
            "Kingdom → Phylum → Class → Order，看看能不能在<b>大尺度上</b>"
            "粗暴地把病毒分准。这一步只要在<b>大的层面</b>预测准，"
            "就算我迈出了一小步。<br><br>"
            "为此我设计了几处创新：<br>"
            "&nbsp;&nbsp;① <b>OutputInitializer</b>：2 层 Transformer 把基因组里所有 domain 聚成一个上下文 g<br>"
            "&nbsp;&nbsp;② <b>串联 Cascade Decoder</b>：上一层的预测作为下一层的 prefix<br>"
            "&nbsp;&nbsp;③ <b>Affiliate Loss</b>：用 ICTV 父-子矩阵 M 强制层级一致<br><br>"
            "结果：Kingdom 99.7%，Order 90.6%，层级一致性 94.9%（从基线 0.02% 起飞）。"
        ),
        "en": (
            "Returned to the supervised side thread: K→P→C→O hierarchy. "
            "Three innovations: OutputInitializer (2-layer Transformer over domains), "
            "tandem cascade decoder (parent prediction conditions child), "
            "affiliate loss (parent-child consistency via ICTV affinity matrix M). "
            "99.7% Kingdom, 90.6% Order, 94.9% hierarchical consistency."
        ),
        "img": ("fig_pipeline_supervised.png",
                 "Supervised three-stage pipeline"),
    },
    {
        "n": 11,
        "zh_title": "怎么验证它真的学到了进化几何？",
        "en_title": "Did it really learn evolutionary geometry?",
        "zh": (
            "<b>实验 A：突变身份 vs 突变数量</b><br>"
            "把 ESM-2 距离拆成 Hamming 部分（数突变个数）和 identity 部分（看哪些位点突变）。"
            "结果：SARS-CoV-2 上 Hamming R² ≈ 0.003，identity R² ≈ 0.852，"
            "<b>差 280 倍</b>。在 RSV 和 Dengue 上也成立。"
            "→ ESM-2 关心的是<b>哪些位点突变了</b>，不是<b>多少个位点变了</b>。<br><br>"
            "<b>实验 B：Integrated Gradients 看高权重残基</b><br>"
            "Top-20 残基里有 18 个落在 NTD/RBD（Fisher OR=13.25, p<10⁻⁴）。"
            "这正是抗原工作者会重点关注的位置 —— "
            "模型没人教，自己就找到了正确的地方。"
        ),
        "en": (
            "Decomposing ESM-2 distance: identity R² (0.852) >> Hamming R² (0.003), 280× gap. "
            "ESM-2 cares about WHICH mutations occur, not how many. Integrated Gradients: "
            "18/20 top residues fall in NTD/RBD (Fisher OR=13.25, p<10⁻⁴)."
        ),
        "img": ("fig_mutation_decomp.png", "Mutation identity vs Hamming R²"),
        "img2": ("fig_3d_mapping.png", "IG residues on PDB structure"),
    },
    {
        "n": 12,
        "zh_title": "最后的「狠考」：5% 测试集是我手动出的卷子",
        "en_title": "The final exam: hand-curated 5% test set",
        "zh": (
            "为了避免「跑分好看但其实在背书」，"
            "我把最后的 5% 测试集<b>手动出题</b> —— 涵盖了所有 41 个 Order，"
            "并且<b>故意加入了训练集里没见过的几种病毒</b>，专门看泛化。<br><br>"
            "在这种条件下还能 Order 90.6% / Top-5 98.9%，"
            "说明模型不是在记忆，而是真的捕到了几何。"
        ),
        "en": (
            "Final 5% test set is hand-curated, covers all 41 Orders, and intentionally "
            "includes families absent from training — to stress generalization rather than "
            "memorization. Order accuracy still 90.6% / Top-5 98.9%."
        ),
        "img": ("fig_tsne_ranks.png", "Per-rank t-SNE of decoder features"),
    },
    {
        "n": 13,
        "zh_title": "整个故事一句话",
        "en_title": "The story in one sentence",
        "zh": (
            "<b>「同一个冻结的蛋白语言模型，"
            "既能粗粒度认出新病毒是什么科目，"
            "也能细粒度看出哪条 SARS-CoV-2 序列是重组体 —— "
            "全程不需要为任何任务专门训练 backbone。」</b><br><br>"
            "如果回到 2019 年武汉，这套流程可以在几分钟内给出："
            "（1）这病毒最像 Coronaviridae，"
            "（2）它的 Spike 跟 SARS-CoV-1 共享了哪些关键残基，"
            "（3）哪些已知抗原可能交叉。"
        ),
        "en": (
            "One frozen PLM — coarse-grained virus identification AND fine-grained "
            "recombinant detection — without task-specific backbone training. "
            "Replayed on Wuhan 2019, this pipeline would give taxonomic placement, "
            "shared functional residues, and candidate cross-reactive antigens within minutes."
        ),
        "img": None,
    },
]


# ─── HTML template ───────────────────────────────────────────────────────────
CSS = """
:root { --fg:#1a1a1a; --muted:#666; --accent:#0f3460; --en-color:#5a6c7d;
        --bg:#fbfbfb; --card:#fff; --border:#e5e7eb; }
* { box-sizing:border-box; }
body { margin:0; padding:0; background:var(--bg); color:var(--fg);
       font-family:-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
       line-height:1.75; font-size:16px; }
.container { max-width:840px; margin:0 auto; padding:48px 28px 80px; }
header { border-bottom:2px solid var(--accent); padding-bottom:24px; margin-bottom:32px; }
h1 { font-size:28px; color:var(--accent); margin:0 0 8px; line-height:1.3; }
h1 .en { display:block; font-size:16px; color:var(--en-color); font-weight:400;
        margin-top:6px; font-style:italic; }
.meta { color:var(--muted); font-size:14px; }
.section { background:var(--card); border:1px solid var(--border);
           border-radius:10px; padding:24px 28px; margin-bottom:18px;
           box-shadow:0 1px 3px rgba(0,0,0,.04); }
.section h2 { font-size:19px; color:var(--accent); margin:0 0 4px;
              border-left:4px solid var(--accent); padding-left:12px; }
.section h2 .num { display:inline-block; background:var(--accent); color:#fff;
                   font-size:13px; padding:2px 8px; border-radius:10px;
                   margin-right:10px; vertical-align:middle; }
.section h2 .en { display:block; font-size:14px; color:var(--en-color);
                  font-weight:400; font-style:italic; padding-left:16px;
                  margin-top:2px; }
.zh { margin:14px 0 6px; }
.en-cap { font-size:14px; color:var(--en-color); font-style:italic;
          border-left:3px solid #d0d7de; padding:6px 0 6px 12px;
          margin:10px 0 6px; background:#f6f8fa; border-radius:0 4px 4px 0; }
.fig-cap { text-align:center; font-size:13px; color:var(--muted);
           margin:-4px 0 8px; font-style:italic; }
footer { margin-top:48px; padding-top:20px; border-top:1px solid var(--border);
         color:var(--muted); font-size:13px; text-align:center; }
b { color:#0f3460; }
i { color:#5a6c7d; }
"""


def section_html(s: dict) -> str:
    parts = [f'<div class="section">']
    parts.append(
        f'<h2><span class="num">{s["n"]}</span>{s["zh_title"]}'
        f'<span class="en">{s["en_title"]}</span></h2>'
    )
    parts.append(f'<div class="zh">{s["zh"]}</div>')
    parts.append(f'<div class="en-cap">EN · {s["en"]}</div>')
    if s.get("img"):
        name, alt = s["img"]
        parts.append(img(name, alt))
        parts.append(f'<div class="fig-cap">Figure · {alt}</div>')
    if s.get("img2"):
        name, alt = s["img2"]
        parts.append(img(name, alt))
        parts.append(f'<div class="fig-cap">Figure · {alt}</div>')
    parts.append("</div>")
    return "\n".join(parts)


html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>ESM-2 病毒进化几何 · 给 TA 的简单易懂版</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<header>
  <h1>ESM-2 病毒进化几何 · 给 TA 的简单易懂版
    <span class="en">Frozen Protein Language Models Encode Viral Evolutionary Geometry —
    a story-style walkthrough for the TA</span>
  </h1>
  <div class="meta">作者 · James Huang &nbsp;|&nbsp;
    完整 ICLR 报告：<code>paper/iclr2026/esm_viral_evolution.pdf</code></div>
</header>

{"".join(section_html(s) for s in SECTIONS)}

<footer>
  双语图文版 · 按作者本人叙述顺序整理 · 配图均来自 ICLR 2026 报告原图<br>
  Bilingual narrative walkthrough · ordered by the author's own first-person telling
</footer>
</div>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(f"[OK] Saved {OUT}  ({len(html)/1024:.1f} KB)")
