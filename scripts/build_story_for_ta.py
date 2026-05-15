"""Build TWO self-contained HTML versions of the story for the TA — one
Chinese-only, one English-only. Images are base64-embedded so each file is
fully portable.

Outputs: ../story_for_TA_zh.html  and  ../story_for_TA_en.html
"""
from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "paper" / "iclr2026" / "figures"
OUT_ZH = ROOT / "story_for_TA_zh.html"
OUT_EN = ROOT / "story_for_TA_en.html"


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
        "n": 1,
        "zh_title": "我去年踩过的坑：序列比对 + 随机森林",
        "en_title": "Last year's attempt: alignment + random forest",
        "zh": (
            "去年我做过一个类似的工作 —— 把 8 种病毒序列做 alignment，"
            "然后用随机森林画出一张「病毒地图」。当时跑完图就开始怀疑：<br><br>"
            "<b>这种纯序列相似度聚出来的图，真的有参考性吗？</b><br><br>"
            "答案是没有。它既看不出哪个病毒「特别」，也回答不了任何生物学问题，"
            "只是把序列上长得像的东西堆在一起。下面这张就是典型的"
            "alignment + PCA + K-means baseline —— 视觉上看着挺干净，"
            "但这种 pipeline 本身有<b>预设</b>：它假定不同序列在同一坐标位置上是「同源」的、"
            "而且这些位置之间的距离可以直接相加；这套假设在高变异、含 indel、含重组的病毒"
            "序列上经常不成立。<br><br>"
            "更基本的一点是：<b>「序列空间」本身就不是一个朴素的欧氏空间</b>——"
            "把序列硬投到 2D PCA 上，距离的几何意义是模糊的；"
            "一张看起来干净的 cluster 图，并不意味着背后的度量真的对应了生物学。"
        ),
        "en": (
            "Alignment-based clustering looks clean, but the pipeline carries strong "
            "assumptions: it treats positions across sequences as homologous and assumes "
            "those positions' contributions to distance simply add up. Both assumptions "
            "break for novel, highly divergent, or recombinant sequences. More fundamentally, "
            "sequence space is not a naive Euclidean space — a clean-looking 2D cluster "
            "plot does not imply the underlying metric is biologically meaningful."
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
        "zh_title": "Embedding 被神化了？PCA 直接降维：真的乱成一团",
        "en_title": "PCA on raw embeddings: literally a mess",
        "zh": (
            "现在的风气是把 embedding 当万能钥匙。我直接拿 ESM-2 的原始 embedding "
            "做 PCA 降到 2D —— 结果如下图，<b>PC1 / PC2 上各种 lineage 完全糊在一起</b>，"
            "根本没有肉眼可见的 cluster 结构。<br><br>"
            "经验上看：原始 ESM-2 空间里的<b>直接欧氏距离</b>并不能稳定地反映 lineage 关系；"
            "PCA 抓到的是<b>方差最大</b>的方向，而方差最大的方向不一定就是承载 lineage 信号的方向。"
            "这也是我后面所有方法的出发点。"
        ),
        "en": (
            "Plain PCA on raw ESM-2 embeddings: lineages are visually tangled in PC1/PC2. "
            "Empirically, raw Euclidean distance in ESM-2 space does not stably reflect "
            "lineage relationships, and the directions of maximum variance are not "
            "necessarily the directions that carry lineage signal."
        ),
        "img": ("fig_raw_pca_messy.png", "Raw ESM-2 PCA 2D — no visible clusters"),
    },
    {
        "n": 7,
        "zh_title": "「作弊」一下：用 LDA 看簇藏在哪里",
        "en_title": "Cheating with LDA to locate the signal",
        "zh": (
            "肉眼看不见，那我就作弊 —— 用 <b>LDA</b>（监督的线性判别分析）"
            "直接问：可分簇信息在哪个方向上？<br><br>"
            "下面这张图是结论：左边 PCA 完全糊住，右边 LDA 直接<b>把各 lineage 分开</b>。"
            "进一步看 PCA 各个分量，真正承载信号的<b>不是 PC1/PC2，而是大概 PC4–PC8</b>。"
            "并且 layer-wise LDA 显示这个信号<b>从 Layer 1 就在了</b> —— "
            "不是深层涌现，而是预训练表征里本就埋着。"
        ),
        "en": (
            "LDA finds the discriminative axes that PCA misses. Signal lives around "
            "PC4–PC8, and Layer-1 LDA already reaches ~95% accuracy — this geometry "
            "is pretraining-encoded, not deep emergence."
        ),
        "img": ("fig_pca_vs_lda.png", "PCA (messy) vs LDA (clean) on the same embeddings"),
        "img2": ("fig_layerwise_lda.png", "Layer-wise LDA probe accuracy"),
    },
    {
        "n": 8,
        "zh_title": "随手记的小疑问：大家用 ESM-2 都在干什么？",
        "en_title": "Side note: what is everyone doing with ESM-2 anyway?",
        "zh": (
            "做到这里我在纸条上记了一段：<br><br>"
            "<i>「目前用 ESM-2 的工作，要么有监督要么无监督，效果参差。"
            "印象里有德国一组的报告说他们试出来效果很差。"
            "本质上大家都还是在<b>找一个把高维表征降到可视的方法</b>，"
            "而且每一步都需要<b>人为主观地引导</b>（选哪一层、选哪些维度、用什么距离）。"
            "那能不能让模型自己把分布说清楚？」</i><br><br>"
            "这是当时的<b>支线疑问</b>，不是主线 —— 主线先把无监督方法跑通。"
            "（这个支线后来直接催生了我那套层级有监督设计，见 §10。）"
        ),
        "en": (
            "Side note on the literature: ESM-2 has been used both supervised and "
            "unsupervised with mixed results (one German group reportedly reported poor "
            "performance). Most approaches still rely on human-guided dimensionality "
            "reduction — pick the layer, pick the dimensions, pick the metric. "
            "Could the model express its own structure? This side thread later became "
            "the hierarchical supervised design in §10."
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
            "<b>最后赢的是 SVD-HDBSCAN</b>：先截断 SVD 去掉那些「方差大但不携带 lineage 信号」"
            "的 nuisance 维度（验证了第 6 节的经验观察），再用 HDBSCAN 的密度聚类。"
            "结果 silhouette = 0.895，ARI = 0.992，没有用任何 lineage 标签。<br><br>"
            "<b>关键的事情发生在「噪声点」上。</b>算法把 329 条序列标为 noise（说「我不确定这是谁」）。"
            "为了知道这些 noise 到底是垃圾还是金子，<b>我亲自一条一条把它们打到 NCBI Virus 数据库里手动核对</b>，"
            "同时用 <b>Nextclade v3.21.2</b> 对每条做 Pango lineage 分配 —— "
            "这是<b>第三方独立工具 + 人工逐条手查</b>双重验证，不是模型自报。<br><br>"
            "结果其中 <b>19 条被官方确认为重组株</b>（X 开头命名 = 真重组）："
            "下面那张 NCBI Virus 截图就是 19 条之一 OY290850.1 → XBB.1.16 的手查留痕。<br><br>"
            "<table style='border-collapse:collapse;margin:8px 0;font-size:13px;'>"
            "<tr style='background:#f0f4f8;'>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>类别</th>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>分支</th>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>数量</th></tr>"
            "<tr><td rowspan='4' style='border:1px solid #d0d7de;padding:4px 10px;'>XBB 系列</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.5（含 .18/.23/.24）</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>8</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.16（含 .19/.2）</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>3</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.9.1, XBB.1.41.1, XBB.2.3(.1)</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>5</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>合计 XBB</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'><b>16</b></td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>其它重组</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;'>XCH.1, XE, XZ</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>3</td></tr>"
            "<tr style='background:#fff7e6;'><td colspan='2' style='border:1px solid #d0d7de;padding:4px 10px;'><b>总计被算法标 noise 且经独立验证的重组株</b></td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'><b>19</b></td></tr>"
            "</table>"
            "<br>"
            "<b>精确率分层看</b>：<br>"
            "&nbsp;&nbsp;• 总体 noise 集（329 条）→ 19/329 = <b>5.8%</b> 命中重组<br>"
            "&nbsp;&nbsp;• 在<b>原本就被人工标为「Other / Recomb.」</b>的 39 条 noise 里 → 18/39 = "
            "<b>46.2%</b> 命中（这是最有意义的子集）<br>"
            "&nbsp;&nbsp;• 在 BA.2/5+ 的 109 条 noise 里 → 1/109，但<b>那唯一一条是 XE 重组株（OX837590）</b>，"
            "原始人工标注「BA.2/5+」漏掉了它，算法替人把它拎了出来<br>"
            "&nbsp;&nbsp;• Delta 的 noise 里命中 0/81 —— 老实说这一类历史经验本来就不容易自动检出，"
            "我不强行解释<br><br>"
            "代表样例：<b>OY290850 = XBB.1.16（2023-06-06 采样）</b>，"
            "可以直接去 NCBI Virus 查证（搜 Accession 即可）。<br><br>"
            "<b>「failure to cluster」不是 bug，而是 feature</b>：算法对说不准的样本诚实地标 noise；"
            "在「Other / Recomb.」这种<b>本来就是杂烩</b>的子集里，近一半的 noise 是真的重组株，"
            "且算法甚至能在错误标注里替人挖出漏掉的 XE。"
        ),
        "en": (
            "Tried every unsupervised method on the menu. Winner: <b>SVD-HDBSCAN</b> — "
            "truncated SVD removes high-variance but lineage-uninformative directions "
            "(confirming the empirical observation from §6), then HDBSCAN runs density "
            "clustering on the compressed space. Silhouette 0.895, ARI 0.992, no lineage "
            "labels used.<br><br>"
            "<b>The interesting thing happens on the 'noise' points.</b> The algorithm "
            "flagged 329 sequences as noise (\"I'm not sure where this belongs\"). To find "
            "out whether these were garbage or gold, <b>I manually looked up every single "
            "noise sequence in the NCBI Virus database, one accession at a time</b>, while "
            "in parallel running <b>Nextclade v3.21.2</b> for Pango lineage assignment on "
            "each — third-party tool plus first-person manual cross-check, not a model "
            "self-report.<br><br>"
            "Among them, <b>19 were officially confirmed as recombinants</b> (the 'X-' "
            "Pango prefix = true recombinant). The NCBI Virus screenshot below shows one "
            "of these manual look-ups: OY290850.1 → XBB.1.16.<br><br>"
            "<table style='border-collapse:collapse;margin:8px 0;font-size:13px;'>"
            "<tr style='background:#f0f4f8;'>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>Group</th>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>Lineage</th>"
            "<th style='border:1px solid #d0d7de;padding:4px 10px;'>Count</th></tr>"
            "<tr><td rowspan='4' style='border:1px solid #d0d7de;padding:4px 10px;'>XBB family</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.5 (incl. .18/.23/.24)</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>8</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.16 (incl. .19/.2)</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>3</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB.1.9.1, XBB.1.41.1, XBB.2.3(.1)</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>5</td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>XBB total</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'><b>16</b></td></tr>"
            "<tr><td style='border:1px solid #d0d7de;padding:4px 10px;'>Other recombinants</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;'>XCH.1, XE, XZ</td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'>3</td></tr>"
            "<tr style='background:#fff7e6;'><td colspan='2' style='border:1px solid #d0d7de;padding:4px 10px;'><b>Total confirmed recombinants in noise set</b></td>"
            "<td style='border:1px solid #d0d7de;padding:4px 10px;text-align:center;'><b>19</b></td></tr>"
            "</table>"
            "<br>"
            "<b>Precision, stratified</b>:<br>"
            "&nbsp;&nbsp;• Whole noise set (329) → 19/329 = <b>5.8%</b> recombinant hit-rate<br>"
            "&nbsp;&nbsp;• Within the 39 noise points already human-labeled as "
            "<b>'Other / Recomb.'</b> → 18/39 = <b>46.2%</b> (the meaningful subset)<br>"
            "&nbsp;&nbsp;• Within the 109 BA.2/5+ noise points → 1/109, but <b>that single "
            "one is an XE recombinant (OX837590)</b> that the human 'BA.2/5+' label had "
            "missed — the algorithm pulled it out on its own<br>"
            "&nbsp;&nbsp;• Within Delta noise → 0/81. Historically this class has been "
            "hard to flag automatically; I will not over-rationalize this<br><br>"
            "Representative example: <b>OY290850 = XBB.1.16 (sampled 2023-06-06)</b>, "
            "verifiable on NCBI Virus by accession lookup.<br><br>"
            "One sentence: <b>'failure to cluster' is a feature, not a bug</b> — "
            "the algorithm honestly flags uncertain samples; within the human-labeled "
            "'Other / Recomb.' bucket (which was always a grab-bag), nearly half of the "
            "noise points are genuine recombinants, and the algorithm can even rescue "
            "an XE that human labels had missed."
        ),
        "img": ("fig_methodology_unsupervised.png",
                 "Unsupervised surveillance methodology"),
        "img2": ("fig_ncbi_verification.png",
                  "NCBI Virus lookup of OY290850.1 → Pango XBB.1.16 — independent manual verification"),
    },
    {
        "n": 10,
        "zh_title": "回到支线：界门纲目，能不能粗犷地分准？",
        "en_title": "Back to the side thread: hierarchical classification",
        "zh": (
            "无监督跑完后，我回到那张纸条上的疑问。<br><br>"
            "高中生物里都学过<b>「界门纲目科属种」</b> —— 这就是生物分类的层级树。"
            "我把这套层级搬到病毒上，做 Kingdom → Phylum → Class → Order 四层预测。"
            "目标很朴素：哪怕只能在<b>大的尺度</b>上分准，也算迈出了一小步。<br><br>"
            "<b>三个我自己挺得意的设计（用大一也能懂的说法）：</b><br><br>"
            "<b>① OutputInitializer ——「先粗读全文再答题」</b><br>"
            "类比：你做阅读理解，不会上来就看第一段答题，会<b>先把全文扫一遍</b>有个整体印象，"
            "再回头答细节。模型也一样：一个病毒基因组里有十几个 Pfam domain（≈ 十几个段落），"
            "我先用一个 2 层 Transformer 把这十几段「读一遍、做个 320 维的全局摘要 g」，"
            "再让后面的解码器在<b>带着这个摘要的前提下</b>去判断分类。<br><br>"
            "<b>② 串联 Cascade Decoder ——「先选大类，再选小类」</b><br>"
            "类比：考试做单选题，与其一次性 41 选 1，不如先决定<b>「这是动物题还是植物题」</b>，"
            "再缩小到具体哪一种。我让 4 个解码器串成一列：第一个出 Kingdom（2 选 1），"
            "把它的预测当成<b>提示</b>塞给下一个解码器去出 Phylum（9 选 1），"
            "依此类推一直到 Order（41 选 1）。每一步的选择空间都被上一步极大地压缩了。<br><br>"
            "<b>③ Affiliate Loss ——「父子不一致就罚」</b><br>"
            "类比：如果你考试写「这是哺乳动物 → 但它是鸟纲」，老师肯定要扣分，"
            "因为「哺乳动物」下面根本没有「鸟纲」这个分支。我把整个 ICTV 父-子映射矩阵 M 喂给损失函数，"
            "<b>只要模型预测的父子组合在生物学上不可能存在，就直接惩罚</b>。"
            "结果是层级一致性从原本随机的 0.02% 直接飙到 <b>94.9%</b>（涨了 4 个数量级）。<br><br>"
            "最终成绩：Kingdom 99.7%，Phylum 92.9%，Class 92.6%，Order 90.6%。"
        ),
        "en": (
            "Three innovations explained at freshman level: "
            "(1) OutputInitializer — like skimming the whole article before answering: "
            "a 2-layer Transformer summarises all Pfam domains into a 320-d genome context g. "
            "(2) Cascade Decoder — like multi-choice exams where you first pick the big "
            "category then narrow down: 4 decoders chained K→P→C→O, each conditioned on "
            "its parent's prediction. "
            "(3) Affiliate Loss — penalises biologically impossible parent-child combinations "
            "via the ICTV affinity matrix M, lifting hierarchical consistency from 0.02% to 94.9%."
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
            "我把最后的 5% 测试集<b>手动出题</b>：涵盖了所有 41 个 Order，"
            "并且<b>有意加入了若干训练集里没见过、但已经被公共卫生界确认为高风险的病毒</b>"
            "（具体名单见 §References / 数据来源），重点测<b>泛化</b>而不是死记硬背。<br><br>"
            "在这种条件下还能 Order 90.6% / Top-5 98.9%，"
            "说明模型捕到的是几何，而不是把训练样本背下来。"
        ),
        "en": (
            "Final 5% test set is hand-curated, covers all 41 Orders, and intentionally "
            "includes several high-risk pathogens not present in training (see References) — "
            "designed to stress generalization. Order accuracy 90.6% / Top-5 98.9%."
        ),
        "img": ("fig_tsne_ranks.png", "Per-rank t-SNE of decoder features"),
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
.body { margin:14px 0 6px; }
.fig-cap { text-align:center; font-size:13px; color:var(--muted);
           margin:-4px 0 8px; font-style:italic; }
footer { margin-top:48px; padding-top:20px; border-top:1px solid var(--border);
         color:var(--muted); font-size:13px; text-align:center; }
b { color:#0f3460; }
i { color:#5a6c7d; }
"""


def section_html(s: dict, lang: str) -> str:
    title = s["zh_title"] if lang == "zh" else s["en_title"]
    body = s["zh"] if lang == "zh" else s["en"]
    fig_label = "图" if lang == "zh" else "Figure"
    parts = ['<div class="section">']
    parts.append(f'<h2><span class="num">{s["n"]}</span>{title}</h2>')
    parts.append(f'<div class="body">{body}</div>')
    if s.get("img"):
        name, alt = s["img"]
        parts.append(img(name, alt))
        parts.append(f'<div class="fig-cap">{fig_label} · {alt}</div>')
    if s.get("img2"):
        name, alt = s["img2"]
        parts.append(img(name, alt))
        parts.append(f'<div class="fig-cap">{fig_label} · {alt}</div>')
    parts.append("</div>")
    return "\n".join(parts)


HEADERS = {
    "zh": {
        "lang": "zh-CN",
        "title": "ESM-2 病毒进化几何 · 给 TA 的故事版",
        "h1": "ESM-2 病毒进化几何 · 给 TA 的故事版",
        "meta": "作者 · James Huang",
        "footer": "按作者本人叙述顺序整理",
    },
    "en": {
        "lang": "en",
        "title": "ESM-2 Viral Evolution — Story Version for the TA",
        "h1": "Frozen Protein Language Models Encode Viral Evolutionary Geometry "
               "— story-style walkthrough for the TA",
        "meta": "Author · James Huang",
        "footer": "Ordered by the author's first-person telling",
    },
}


def build(lang: str, out_path: Path) -> None:
    h = HEADERS[lang]
    body = "".join(section_html(s, lang) for s in SECTIONS)
    html = f"""<!DOCTYPE html>
<html lang="{h['lang']}">
<head>
<meta charset="UTF-8">
<title>{h['title']}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<header>
  <h1>{h['h1']}</h1>
  <div class="meta">{h['meta']}</div>
</header>
{body}
<footer>{h['footer']}</footer>
</div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"[OK] Saved {out_path}  ({len(html)/1024:.1f} KB)")


if __name__ == "__main__":
    build("zh", OUT_ZH)
    build("en", OUT_EN)
