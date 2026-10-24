# OpenSpec Strategy 场景检查

以下均为静态场景推演及预期行为，不是已经执行的 OpenSpec 或 Focus Loop 测试。

## 应采用：按 capability 逐步形成开发变更

输入：用户希望为现有 agent 增加上传文件能力，尚未建 change；先只读架构，再逐个确认 proposal、specs、design、tasks。

预期：复用已有相关 Context；需要调查时用 explore，若只缺 baseline 背景则直接读取。继承有效 main specs、当前代码与用户范围；new 只 scaffold 并停止；收到下一步方向后 continue 一次一个工件并停止。每次等真实前置工件出现，不固定新建七个 Context。用户批准实施后才 apply。verify 的只报告边界与 sync/archive 各自授权独立判断。当前授权工作结束或原 Skill 要求等待时停止。

## 不应重复采用：当前证据已充分

输入：用户询问上传链路的规范与实现是否一致；同一代码、工件和评价范围已有充分 verify 报告，Context 也已掌握架构。

预期：直接引用有效报告和版本回答，不重新 explore、不重新 new、不重复 verify，不为策略名称派生 Context。发现覆盖缺口才安排范围明确的检查。继承报告来源与限制；问题回答充分时停止。

## 收到反馈：实施中改为按用户隔离路径

输入：apply 已完成若干任务，用户明确决定把共享工作区改为按用户隔离，并引用旧版 spec。

预期：Patrol 识别新决定与旧决定的替代关系，复用原工作线，传递所引用文件的真实版本。核对受影响 capability、spec/design/tasks、调用代码、测试和已同步 main spec；暂停依赖旧路径的实施，保留独立成果。按授权修订再恢复；原 Run 未实际停止时不谎称已停止。重验失效范围并重新比较同步差异；不从 new 全部重跑。缺关键决定或已到用户停止边界时等待。

## 停止边界：new 与 continue

输入：用户只要求新建 scaffold；后来只批准生成 proposal。

预期：new 展示首个模板后停止；continue 仅创建首个就绪工件并停止；不能新起 Run 绕过等待而生成所有工件或实施。保留已明确 change，不向用户要求线程选择。

## 目标选择与源文缺失

输入：多个活动 changes，用户说“验证一下”；或只有 STRATEGY.md，找不到完整 verify Skill。

预期：通过 Patrol 澄清具体变更对象，不按最近修改时间猜测。缺原文时报告实际缺失，不照策略摘要执行，也不声称资源目录已被 Focus 自动安装。

## 同步冲突与横向扩展

输入：两个 change 修改同一 main requirement，其中一项已同步，另一项只增加一个场景。

预期：协调同一 main spec 的写入归属，读取最新 delta/main 双方内容，横向内容合入原 requirement，保留未涉及的场景。不能把旧比较当最新比较；未变的已同步结果不重复写入；含义冲突则澄清后再合并。

## 验证降级与证据失效

输入：只有 tasks，缺 specs/design，未执行测试；或已有报告后代码发生相关变化。

预期：前者只报告实际覆盖任务检查并列明跳过项，不能声称三维全部通过或测试通过；后者标出报告失效范围，只重验变化与覆盖缺口。报告产生不自动授权修复。

## 归档例外

输入：任务未全完成，用户要求归档，并在阅读告警和同步摘要后明确确认跳过同步。

预期：保留原 Skill 允许确认后带告警归档的边界，记录未完成项、同步跳过和风险，不写成验收通过。没有 verify 就注明未验证。目标路径已存在则停止，不覆盖。用户若选择同步，按原 Skill 委派完整 sync 并核实真实结果；失败不冒充同步成功。

## workspace-planning 约束

输入：CLI 返回 workspace-planning，apply 的 allowedEditRoots 为空；或者当前选择 verify/sync/archive。

预期：按对应 Skill 原文停止，不回退仓库路径、不修改关联仓库、不因单入口策略绕开限制。继承真实 actionContext 与待用户解决的范围。

## 静态检查与未执行项

- 已用目标 Focus 源码的 parse_strategy 解析成功；精确存在 applicability、evolution、inheritance 三段，元信息、ID、版本和长度符合当前合同。
- 七份资源快照与源文件逐字节及 SHA-256 一致；源文未修改，sync 本地定制规则保留。
- 检查仅引用七个 Skill，没有引入批量生成或额外的更新入口。
- 未执行上述动态场景、OpenSpec 命令、实际开发/归档、Focus 模型预演、Loop 调度或目标项目验收。
