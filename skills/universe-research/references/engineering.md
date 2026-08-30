# 工科

Agent 判定本题为工科后阅读本文件。Agent 不得把本文件的检索角度用于计算机科学或医学。

工科文献研究的检索角度取自工程设计文献中的既定用语。ScienceDirect 将 design considerations 定义为影响产品发展的因素，包括产品性质、工艺设计与最终使用性能。IEEE 与工程综述常用 state of the art、design requirements、constraints、specifications、trade-off、prototype 与 validation。国内工科毕业设计与开题文献综述常用设计要求、技术参数、设计标准与可行性。

Autoverse 的 `search --domain` 只有 `auto`、`medicine` 与 `computer_science`。Agent 检索工科文献时使用 `--domain auto`。Agent 不得膮造 `--domain engineering`。

## 检索

```text
autoverse --json --quiet search "<engineering question>" --domain auto
autoverse --json --quiet search "<engineering question>" --domain auto --type review
autoverse --json --quiet resolve doi:<doi>
autoverse --json --quiet resolve arxiv:<xxxxxxxx>
```

Agent 将总问题拆为互补的检索角度，例如工程问题与设计对象、设计要求、约束条件、技术方案或设计方法、性能指标与技术参数、权衡、原型或实验验证、技术标准、争议与近年进展。装置、材料、工艺、结构、控制方案与技术标准编号的别名均须纳入检索式。

文献来源中写「Autoverse 文献检索，含预印本」。

## 主题各节

Agent 按设计对象、设计要求、约束条件、技术方案、性能指标、权衡或验证方式组织主题各节。读后文所需的问题表述、符号与单位，并入引言或本节开头。Agent 不单列 Background。

## 著录

技术标准首次出现写中文标准名称，后括标准编号。

## 用词

现有技术水平，不用「最先进」。设计要求，不用「需求」。约束条件，不用「限制」。技术规格，不用「说明书式规格」。权衡，不用「折中」。原型，不用「样机」硬套所有对象。验证指对照规格检查实现是否正确。确认指检查是否解决了正确的工程问题。二者不得混用。
