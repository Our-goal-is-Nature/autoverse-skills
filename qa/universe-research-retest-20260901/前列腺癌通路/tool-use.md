# tool-use

本次任务文件：`/tmp/pca-pathway-20260901/pca-pathway-ids-20260901.txt`

## 账户

1. `autoverse --json --quiet whoami`  
   带 year-from/year-to：否。返回篇数：不适用。年份 min/max：不适用。退出码 0。

## 主题检索（均 `--domain medicine`，均带默认起止年）

2. `autoverse --json --quiet search "prostate cancer signaling pathway androgen receptor PI3K Wnt review" --domain medicine --year-from 2022 --year-to 2026 --type review --limit 20`  
   带 year-from/year-to：是。返回篇数：20。年份 min/max：2021/2026。退出码 0。

3. `autoverse --json --quiet search "prostate cancer prostate carcinoma PCa androgen receptor AR signaling pathway mechanism castration-resistant CRPC" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：20。年份 min/max：2023/2026。退出码 0。

4. `autoverse --json --quiet search "prostate cancer PI3K phosphatidylinositol 3-kinase AKT mTOR PTEN PIK3CA pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：20。年份 min/max：2022/2026。退出码 0。

5. `autoverse --json --quiet search "prostate cancer Wnt beta-catenin β-catenin CTNNB1 signaling pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：20。年份 min/max：2022/2026。退出码 0。

6. `autoverse --json --quiet search "castration-resistant prostate cancer CRPC AR-V7 androgen receptor splice variant neuroendocrine NEPC signaling pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`（retryable）。

7. `autoverse --json --quiet search "prostate cancer AR PI3K AKT pathway crosstalk resistance enzalutamide abiraterone" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`（retryable）。

8. `autoverse --json --quiet search "prostate cancer DNA damage repair homologous recombination PARP BRCA ATM signaling pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 20`  
   带 year-from/year-to：是。返回篇数：1。年份 min/max：2025/2025。退出码 0。

9. 第 6 条同式重试一次。  
   带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`。其后停止该检索式。

10. 第 7 条同式重试一次。  
    带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`。其后停止该检索式。

11. `autoverse --json --quiet search "prostate cancer PTEN deletion PI3K AKT mTOR signaling castration-resistant" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`（retryable）。

12. `autoverse --json --quiet search "prostate cancer homologous recombination BRCA2 PARP inhibitor olaparib DNA repair pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：8。年份 min/max：2022/2025。退出码 0。

13. 第 11 条同式重试一次。  
    带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`。其后停止该检索式。

14. `autoverse --json --quiet search "prostate cancer MAPK ERK RAS RAF signaling pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：2。年份 min/max：2023/2025。退出码 0。

15. `autoverse --json --quiet search "prostate cancer TGF-beta TGF-β SMAD signaling epithelial mesenchymal" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：10。年份 min/max：2021/2026。退出码 0。

16. `autoverse --json --quiet search "neuroendocrine prostate cancer NEPC lineage plasticity signaling RB1 TP53" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：5。年份 min/max：2023/2026。退出码 0。

17. `autoverse --json --quiet search "castration-resistant prostate cancer Hippo YAP TEAD Hedgehog Notch signaling pathway" --domain medicine --year-from 2022 --year-to 2026 --limit 15`  
    带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`（retryable）。

18. 第 17 条同式重试一次。  
    带 year-from/year-to：是。返回篇数：0。年份 min/max：无。退出码 1。错误码：`ALL_SOURCES_UNAVAILABLE`。其后停止该检索式。

## 题名核验（完整题名，不带起止年）

19. `autoverse --json --quiet search "Reciprocal feedback regulation of PI3K and androgen receptor signaling in PTEN-deficient prostate cancer" --domain medicine --limit 10`  
    带 year-from/year-to：否。返回篇数：2。年份 min/max：2011/2017。退出码 0。纳入题名匹配篇：2011，Cancer Cell。

20. `autoverse --json --quiet search "AR-V7 and resistance to enzalutamide and abiraterone in prostate cancer" --domain medicine --limit 10`  
    带 year-from/year-to：否。返回篇数：10。年份 min/max：2014/2024。退出码 0。纳入题名匹配篇：2014，New England Journal of Medicine。

21. `autoverse --json --quiet search "DNA-Repair Defects and Olaparib in Metastatic Prostate Cancer" --domain medicine --limit 10`  
    带 year-from/year-to：否。返回篇数：10。年份 min/max：2015/2024。退出码 0。纳入题名匹配篇：2015，New England Journal of Medicine。

## 核验

22. `autoverse --json --quiet batch -f /tmp/pca-pathway-20260901/pca-pathway-ids-20260901.txt`  
    带 year-from/year-to：否。返回篇数：29（全部成功）。年份 min/max：2011/2026。退出码 0。

未调用医学补充路径 `/v1/pubmed/articles/summary` 与 `/v1/pubmed/articles/detail`。未改写默认起止年。

## 文末统计

- 纳入总篇数：29
- 2022–2026 篇数：26
- 基础论文题名：
  1. Reciprocal Feedback Regulation of PI3K and Androgen Receptor Signaling in PTEN-Deficient Prostate Cancer（2011）
  2. AR-V7 and Resistance to Enzalutamide and Abiraterone in Prostate Cancer（2014）
  3. DNA-Repair Defects and Olaparib in Metastatic Prostate Cancer（2015）
- 主题检索次数：17（全部带 `--year-from 2022 --year-to 2026`）
- 题名核验次数：3
- batch 次数：1
- 是否改写默认起止年：否
