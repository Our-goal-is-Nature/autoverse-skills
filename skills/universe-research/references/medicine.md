# 医学

Agent 判定本题为医学后阅读本文件。Agent 不得把本文件的检索角度用于计算机科学或工科。综述不构成个体诊疗建议。Agent 只在对话中说明这一点。Agent 不把该说明写进综述标题或开篇。

## 检索

Agent 使用 `--domain medicine`。

```text
autoverse --json --quiet search "<clinical question>" --domain medicine
autoverse --json --quiet search "<clinical question>" --domain medicine --type review
autoverse --json --quiet resolve <prefixed-id>
```

Agent 将总问题拆为互补的检索角度，例如机制、疗效、方法、结局、争议与近年进展。基因、药物、疾病的别名均须纳入检索式。

文献来源中写「Autoverse 医学文献检索」。

精选命令未返回被引次数或医学题录时，Agent 在共用路径之外只可再调用下列路径。

```text
autoverse --json --quiet api -X GET /v1/pubmed/articles/summary
autoverse --json --quiet api -X GET /v1/pubmed/articles/detail
```

## 主题各节

Agent 按机制、通路、亚型或争议组织主题各节。

## 著录

药物首次出现用中文通用名，后括英文。Agent 不得编造 PMID。

## 用词

通路交叉或信号串扰，不用「交叉对话」。现有治疗仍难以覆盖的情形，不用「未满足需求」。细胞周期以外的作用，不用「周期外」。
