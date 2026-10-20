# Strategy

**Focus 官方 Strategy 生态仓库：分享、安装和复用上下文演化的工作策略。**

> Skill teaches an Agent how to work. Strategy teaches Focus how to evolve the work.

Skill 教会 Agent 完成一件事；Strategy 帮助 Focus 随着任务变化组织、派生、验证和汇合工作。用户始终通过 Patrol 的单入口表达目标与反馈，无需管理执行线程。

本仓库提供可导入的策略、编写模板、贡献规范和格式校验工具，兼容 [Focus](https://github.com/Leeminjing/Focus) 的 `focus.strategy/v1` 合同。策略是 Patrol 的决策参考；实际决策、权限、执行和验收由 Focus 负责。

## 安装与使用

1. 在下方选择方法，下载对应目录里的 `STRATEGY.md`，或复制完整文件内容。
2. 打开 Focus 的 **记忆库 → Strategy · 工作策略 → 导入策略**。
3. 选择文件或粘贴内容，选择全局或工作区，预览后安装并按需启用。
4. 继续向 Patrol 表达目标，也可以说“这次按‘先验证关键假设’推进”。启用表示允许考虑，实际采用仍取决于工作状态。

工作区同 ID 安装整份覆盖全局安装，包括停用设置。同 ID 更新先预览差异再替换；本地修改请先导出备份。更新从后续冻结轮次生效。v1 使用文件或粘贴导入，尚不支持 GitHub URL 直接安装和自动更新。

## 策略目录

按工作方法组织，每份策略独立目录，保持已有分享 ID 稳定。

| 工作方法 | Strategy | 适用局面 |
| --- | --- | --- |
| 探索 | [独立探索](strategies/explore/STRATEGY.md) | 未确定的新想法需要独立考察 |
| 探索与交付 | [探索验证实施](strategies/explore-validate-build/STRATEGY.md) | 模糊目标、关键未知项与逐步交付 |
| 验证 | [先验证关键假设](strategies/validate-before-build/STRATEGY.md) | 先用最小验证减少返工 |
| 竞争性派生 | [竞争性派生](strategies/compete/STRATEGY.md) | 从共同基线比较真实候选 |
| 诊断与重构 | [诊断—重构](strategies/diagnose/STRATEGY.md) | 用户否定方案，先查明原因 |
| 拆分 | [任务拆分](strategies/split/STRATEGY.md) | 职责独立、依赖明确的工作 |
| 调整 | [决策变更](strategies/revise/STRATEGY.md) | 新决定替代旧决定 |
| 汇合 | [综合汇合](strategies/combine/STRATEGY.md) | 整合真实成果、保留差异与来源 |

探索、验证和实施是可能的 Context 演化结果。Patrol 可以继续已有 Context、按真实依赖并行推进，也可以在证据充分时停止扩张。

## 编写一份 Strategy

复制 [模板](templates/strategy/STRATEGY.md) 到 `strategies/<method>/STRATEGY.md`，使用自己的 `namespace/name` ID，填写三个部分：

- **applicability**：什么局面适用，什么情况不必采用。
- **evolution**：何时继续或派生 Context，如何响应反馈、等待证据、汇合与停止。
- **inheritance**：继承哪些有效目标、约束、版本与证据，排除哪些过时要求，保留哪些不确定性。

仅使用 `schema`、`id`、`name`、`description`、`version` 元信息；`description` 可选。三段正文各最多 12000 字符，元信息最多 8000 字符，文件最多 160000 UTF-8 字节。更多规则见 [贡献规范](CONTRIBUTING.md) 和 [Focus 编写说明](https://github.com/Leeminjing/Focus/blob/main/docs/strategies/README.md)。

## 本地检查

需要 Python 3.11+。

```sh
python -m pip install -r requirements.txt
python -m tools.validate
python -m unittest discover -s tests -v
```

校验单份文件：`python -m tools.validate strategies/explore/STRATEGY.md`。CI 检查文件合同、ID 唯一性、模板和场景材料结构。解析代码提取自固定版本的 Focus，来源与更新方式见 [tools/README.md](tools/README.md)。

**格式有效不等于策略行为已验证。** [场景材料](tests/scenarios.json) 为每份方法提供“应该采用 / 不必采用 / 收到新反馈”三类输入与评审标准。请在 Focus 编辑器执行预演并在 PR 中记录结果；预演本身也不替代真实执行验收。

## 从 Skill 迁移

保留 Skill 的具体执行方法，从中提炼适用条件、演化规则和继承规则。不要机械改名或复制工具权限。首版提供 [迁移指南](docs/skill-migration.md)；辅助迁移工具留待 V2。

## 路线与边界

- **V1**：策略集合、模板、贡献规范、格式 CI、场景评审材料。
- **V2**：Skill → Strategy 辅助迁移工具。
- **V3**：在 Focus 中实现策略浏览、GitHub 安装与更新提醒。

Strategy 不授予直接调用 Kernel、绕过 Verifier 或跳过用户授权的能力，也不保存任务进度或提供执行保证。每轮安排应依据最新有效要求、Observation 和真实结果重新判断。

本仓库采用 [Apache-2.0](LICENSE)。七份初始示例来自 Focus，详见 [来源记录](NOTICE)。欢迎通过 [PR](CONTRIBUTING.md) 贡献方法和场景。
