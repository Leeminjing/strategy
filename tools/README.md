# 作者工具与合同来源

`python -m tools.validate` 递归检查 `strategies/` 和 `templates/` 的 `STRATEGY.md`，拒绝无效文件、缺失输入和重复 ID，失败时返回非零退出码。也可以传入一个或多个文件或目录。

共享解析入口统一使用：

```python
from tools.focus_contract import parse_strategy

package = parse_strategy(markdown)
print(package.metadata.id)
```

`focus_contract.py` 提取自 Focus 提交 [`86905480be322d8a36c0a2df36e1469450fa22fd`](https://github.com/Leeminjing/Focus/tree/86905480be322d8a36c0a2df36e1469450fa22fd)：

- `strategy_packages.py` 中的 `StrategyMetadata`、`_MetadataLoader`、`parse_strategy` 原样保留。
- `evolution_strategies.py` 中的 `EvolutionStrategy` 原样保留。
- `StrategyPackage` 仅保留模型配置和两个字段，移除不需要的导出和 hash 方法。
- 仅保留验证所需的导入，删除对 Focus 运行时的依赖。

没有修改 v1 校验规则。文件头和 [NOTICE](../NOTICE) 记录了来源与提取范围。更新时对照上游代码，保持上述类和函数一致，同步来源提交并运行合同边界与 CLI 集成测试。不要增加一套新的配置语言或执行器。

格式校验不执行策略文档或 Skill，不连接模型，不访问真实工作区。`tests/scenarios.json` 是人工行为评审材料，其结构检查只保证材料齐备；实际推演在 Focus 中完成。
