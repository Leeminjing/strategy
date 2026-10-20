"""Extracted Focus v1 validation contract (Apache-2.0).

Source: https://github.com/Leeminjing/Focus/tree/86905480be322d8a36c0a2df36e1469450fa22fd
See tools/README.md for extraction details. No execution or installation logic.
"""

from __future__ import annotations

import re
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator



class EvolutionStrategy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    applicability: str = Field(min_length=1, max_length=12000)
    evolution: str = Field(min_length=1, max_length=12000)
    inheritance: str = Field(min_length=1, max_length=12000)

    @field_validator("applicability", "evolution", "inheritance")
    @classmethod
    def _nonblank(cls, value):
        if not value.strip():
            raise ValueError("策略正文不能为空白")
        return value


class StrategyMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    schema_version: Literal["focus.strategy/v1"] = Field(default="focus.strategy/v1", alias="schema")
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]{0,63}/[a-z0-9][a-z0-9._-]{0,95}$")
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    version: str = Field(max_length=96, pattern=r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")

    @field_validator("name")
    @classmethod
    def nonblank_name(cls, value):
        if not value.strip():
            raise ValueError("策略名称不能为空白")
        return value


class StrategyPackage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    metadata: StrategyMetadata
    strategy: EvolutionStrategy


class _MetadataLoader(yaml.SafeLoader):
    """元信息只接受普通、唯一字符串键，拒绝 YAML merge/alias。"""

    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError("策略元信息不支持 YAML alias")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError("策略元信息存在非字符串键或重复字段")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def parse_strategy(markdown: str) -> StrategyPackage:
    if len(markdown.encode("utf-8")) > 160_000:
        raise ValueError("策略文件不能超过 160 KB")
    text = markdown.removeprefix("\ufeff").replace("\r\n", "\n")
    header = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not header or len(header[1]) > 8000:
        raise ValueError("策略文件需要 YAML 元信息，且元信息不能超过 8000 字符")
    try:
        metadata = yaml.load(header[1], Loader=_MetadataLoader)
    except (yaml.YAMLError, RecursionError) as exc:
        raise ValueError("策略元信息不是有效的安全 YAML") from exc
    if not isinstance(metadata, dict) or "schema" not in metadata:
        raise ValueError("策略元信息必须声明 schema: focus.strategy/v1")
    body = text[header.end():]
    sections, current, lines, fence = {}, None, [], None
    for line in body.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, tail = marker.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not tail.strip():
                fence = None
        heading = re.fullmatch(r"## (applicability|evolution|inheritance)\s*", line) if fence is None else None
        if heading:
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current, lines = heading[1], []
            if current in sections:
                raise ValueError(f"策略章节重复：{current}")
        elif current is not None:
            lines.append(line)
        elif line.strip():
            raise ValueError("正文必须以 ## applicability、## evolution 或 ## inheritance 开始")
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return StrategyPackage(metadata=StrategyMetadata.model_validate(metadata), strategy=EvolutionStrategy.model_validate(sections))
