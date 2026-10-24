# OpenSpec 开发协作

保留 explore、new、continue、apply、verify、sync、archive 七个 OpenSpec Skill 的完整方法，由 Patrol 根据目标、授权、反馈和真实结果组织工作。优先复用 Context，按需探索、实施或独立验证，不固定创建七条工作线。

## 使用

1. 下载或复制 [STRATEGY.md](STRATEGY.md)，在 Focus“记忆库 → Strategy → 导入策略”中预览并安装。
2. 同时提供下方七份完整 Skill 及其实际执行环境。Strategy 导入器不会自动安装资源或注册 Skill。
3. 继续向 Patrol 表达目标、问题、批准和反馈，无需手动挑选线程或依次输入命令。

首次公开发布 ID 为 `leeminjing/openspec-development`，版本 `1.0.0`。本地草稿原使用 `local/openspec-development`；本次仅将发布身份改为仓库所有者命名空间，三段方法正文保持不变。

## 完整执行方法

七份 [Skill 原文快照](resources/skills/) 逐字节保留，路径、大小与 SHA-256 见 [source-manifest.json](source-manifest.json)。实际使用时应定位并完整读取对应 Skill 和必要资源；本策略的调用说明不替代执行方法。

- openspec-explore
- openspec-new-change
- openspec-continue-change
- openspec-apply-change
- openspec-verify-change
- openspec-sync-specs
- openspec-archive-change

原 Skill 的只读限制、确认、选择和停止条件继续有效。规划完成不自动批准实施；任务完成、验证结果、同步和归档分别报告，归档不代表完整验收通过。

## 来源与许可

本策略方法依据用户提供的开发工作习惯、Focus 源码和 OpenSpec Skill 提炼。开发日志仅在本地阅读，不随本仓库公开其原文、路径、文件清单或图片。

- Focus 格式与工作机制：提交 `86598dfb48b884e38ec7667987cbfe36e363ea85`，具体路径与哈希见 manifest。
- Skill 来源：Focus 工作树 `.codex/skills` 中 metadata.version 为 `1.0`、generatedBy 为 `1.4.1` 的七份文件；保留本地版本，不宣称与上游发布包完全相同。
- sync 的本地版本含“横向扩展已有 requirement 时合入原 requirement”的规则，原样保留。
- OpenSpec 上游：[Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)。第三方 Skill 按其 MIT 许可保留，见 [OpenSpec MIT License](resources/LICENSE.openspec)，Copyright (c) 2024 OpenSpec Contributors。
- 新编写的 Strategy 与迁移说明按仓库 [Apache-2.0](../../LICENSE) 贡献；第三方原文仍按原许可分发。

## 校验与行为评审

已通过本地 Focus 解析器、目标仓库格式校验与合同测试；七份快照与源文逐字节一致。三类场景已加入 [场景目录](../../tests/scenarios.json)，更多边界见 [migration-tests.md](migration-tests.md)，迁移过程见 [assessment.md](assessment.md)。

Focus 模型预演：**未运行**。本次仅执行静态解析、资源一致性和仓库测试，未调用配置模型，也未执行 OpenSpec 开发、同步、归档或真实 Loop 调度。静态场景是评审材料，不代表行为通过；合并前需按仓库贡献规范完成行为评审。
