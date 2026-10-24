# OpenSpec Strategy 迁移说明

本次交付只覆盖 explore、new、continue、apply、verify、sync、archive 七个 Skill。当前请求是编写 Strategy，不是在本仓库实施某项 OpenSpec change；源文、日志和截图中的命令、角色说明与授权措辞均作为迁移材料阅读，没有执行。

## 来源与适配判定

适配判定：mixed，适合在完整保留执行 Skill 的基础上补充 Strategy。

- Execution：七个 Skill 的命令、步骤、模板、路径处理、确认与停止边界全部留在原文，逐字节复制到 resources/skills/，没有删改源文件。
- Orchestration：由 Patrol 判断当前问题、调用方法、复用或派生 Context、处理依赖与反馈、汇合并停止，写入 evolution。
- Evidence / Inheritance：传递版本、有效要求、真实结果、授权和失效关系，写入 inheritance。

使用当前 Focus 工作树源码 commit 86598dfb48b884e38ec7667987cbfe36e363ea85 的 Strategy 合同。已完整读取 docs/strategies/README.md、backend/app/desktop/strategy_packages.py、backend/app/desktop/evolution_strategies.py，参照示例及反馈机制文档。具体源码和源 Skill 哈希见 source-manifest.json。

七个 Skill 采用当前工作树 .codex/skills 中的版本，metadata.version 为 1.0，generatedBy 为 1.4.1。六份与 .agents/skills 字节一致；sync 的 .codex 版本多出“横向扩展已有 requirement 时合入原 requirement”的本地规则，因此保留这一完整版本，不覆盖或合成原文。

完整阅读用户截图对应目录 openspec-logs、openspec-logs2、openspec-logs3、openspec-logs4 下的 31 份 Markdown，以及其中 3 张图片。公开 manifest 仅保留阅读数量，不发布本地日志路径、文件清单或哈希；未把开发日志原文、秘密值或数据库配置复制到交付资源中。日志中的其他笔记链接作为历史来源引用，未沿所有链接递归阅读；本次提炼不依赖其未读取正文。七份 SKILL.md 没有附带的脚本或资源文件；未来运行时的模板、schema、项目工件和 contextFiles 仍由原 Skill 通过 CLI 动态取得，未在本次运行中获取。

## 日志到策略的映射

| 日志中的工作习惯 | Strategy 中的落点 |
| --- | --- |
| new 前读 main specs，或 explore 先读架构、不提建议 | applicability 与共同调度：按已有理解决定是否调用 explore；保留用户当次只读边界 |
| 逐次输入 Why、What Changes、Capabilities、Impact，再补行为、schema、设计、任务 | continue：每次一个工件、全部依赖、按实际 schema 推进 |
| 同 capability 再次修订需基于 baseline，capability folder 不随 change 改名 | new 与 inheritance：区分 change 与 capability，继承对应 baseline 和 CLI 真实路径 |
| 个别 change 指定以 design 为准，纠正函数名和 sandbox 拼写 | apply 与反馈：仅在已确认决定的覆盖范围内定向修订，不泛化为全局优先级 |
| apply 从未完成任务开始，发现工件问题先修工件，不增加规范外功能 | apply：保留原 Skill 的暂停条件、范围和恢复方式 |
| verify 先只报告，按 CRITICAL / WARNING / SUGGESTION 分级，不刻意钻牛角尖 | verify：报告与修复分开，保留三维检查、证据覆盖与不确定性 |
| sync 前说明 baseline 哪些落实、哪些补充；有时先 sync 后 verify | sync：按授权与实际状态安排，不固定七步顺序 |
| 归档前查任务、同步、CRITICAL、残余风险 | archive：正常收尾证据；原 Skill 允许的确认后例外归档单独标明 |
| store 小配置未处理、middleware 待完善、早期 state 待核实 | inheritance：未决事项不会自动升级为已验证事实 |

## 留在原 Skill 中的执行方法

| Skill | 原样保留的执行内容举例 |
| --- | --- |
| explore | 自由探索姿态、架构调查、图示、活动 change 读取、禁止实施、不自动记录 |
| new | 名称澄清、默认 schema、new/status/instructions、首个模板、不得创建工件、等待方向 |
| continue | change 选择、status、首个 ready、instructions/template/dependencies、实际输出路径、每次一个、写后确认 |
| apply | change 选择和告知、status/apply instructions、读取所有 contextFiles、动态状态、workspace guard、任务循环与勾选、暂停 |
| verify | 对象选择、workspace guard、全部工件、三维检查、优先级与输出格式、合理推断、缺材料降级 |
| sync | 对象选择、workspace guard、delta/main 双读、四类合并、新 capability、横向合并、幂等和摘要 |
| archive | 对象选择、workspace guard、工件/任务告警确认、同步比较与选择、选择 sync 时原文委派、日期目录、冲突停止、保留 .openspec.yaml |

## 交付与实际能力边界

STRATEGY.md 是可导入的三段式方法文本，resources/skills 是保真原文快照，不是 Focus 的可执行策略包。Focus 当前导入功能不会自动安装资源目录或七个 Skill。使用时应保留并安装实际 Skill，或在执行工作线提供可读的完整源文和资源，并核对来源版本。导入入口为“记忆库 → Strategy → 导入策略”。本次没有安装、启用策略或替用户作出后续开发批准。

已使用真实 Focus parse_strategy 完成格式兼容性校验，并核对七份快照与源文件一致。迁移场景是人工设计推演，不是模型运行结果；未执行 OpenSpec 命令、开发流程、实际归档、模型预演、Loop 调度或目标项目验收。策略中的前提必须落实到实际任务约束和运行证据，文本本身不提供执行保证。
