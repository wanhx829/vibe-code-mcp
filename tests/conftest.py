import os
import pytest


@pytest.fixture
def resource_dir(tmp_path):
    """Create a minimal vibecodingcn resource structure for testing."""
    zh_prompts = tmp_path / "i18n" / "zh" / "prompts" / "coding_prompts"
    zh_prompts.mkdir(parents=True)

    (zh_prompts / "(1,1)_项目上下文与代码审查.md").write_text(
        "# 项目上下文与代码审查\n\n将自然语言需求转换为结构化项目上下文文档。帮助进行代码审查，发现潜在问题。",
        encoding="utf-8",
    )

    en_prompts = tmp_path / "i18n" / "en" / "prompts" / "coding_prompts"
    en_prompts.mkdir(parents=True)
    (en_prompts / "(1,1)_project_context.md").write_text(
        "# Project Context Generator\n\nGenerate structured project context documents.",
        encoding="utf-8",
    )

    zh_system = tmp_path / "i18n" / "zh" / "prompts" / "system_prompts"
    zh_system.mkdir(parents=True)
    (zh_system / "(1,1)_系统架构分析.md").write_text(
        "# 系统架构分析\n\n分析系统架构，提供优化建议。",
        encoding="utf-8",
    )

    zh_meta = tmp_path / "i18n" / "zh" / "prompts" / "meta_prompts"
    zh_meta.mkdir(parents=True)
    (zh_meta / "(1,1)_提示词优化.md").write_text(
        "# 提示词优化\n\n优化现有提示词，提升效果。",
        encoding="utf-8",
    )

    # External prompt_docs library
    prompt_docs = tmp_path / "libs" / "external" / "prompts-library" / "prompt_docs" / "subdir"
    prompt_docs.mkdir(parents=True)
    (prompt_docs / "架构设计提示词.md").write_text(
        "# 架构设计提示词\n\n帮助进行系统架构设计。",
        encoding="utf-8",
    )

    # Skills
    zh_skills = tmp_path / "i18n" / "zh" / "skills"
    zh_skills.mkdir(parents=True)
    pg_skill = zh_skills / "postgresql"
    pg_skill.mkdir()
    (pg_skill / "SKILL.md").write_text(
        "---\nname: postgresql\ndescription: \"PostgreSQL 专家技能\"\n---\n\n# PostgreSQL 专家\n\nPostgreSQL 数据库最佳实践。",
        encoding="utf-8",
    )
    refs = pg_skill / "references"
    refs.mkdir()
    (refs / "cli.md").write_text("# CLI Reference\n\npsql commands.", encoding="utf-8")

    en_skills = tmp_path / "i18n" / "en" / "skills"
    en_skills.mkdir(parents=True)
    ccxt_skill = en_skills / "ccxt"
    ccxt_skill.mkdir()
    (ccxt_skill / "SKILL.md").write_text(
        "---\nname: ccxt\ndescription: \"Crypto exchange API\"\n---\n\n# CCXT\n\nUnified crypto exchange API.",
        encoding="utf-8",
    )

    # Documents
    zh_docs = tmp_path / "i18n" / "zh" / "documents"
    methodology = zh_docs / "Methodology and Principles"
    methodology.mkdir(parents=True)
    (methodology / "开发经验.md").write_text(
        "# 开发经验\n\n变量命名、文件结构、编码规范、架构原则等实践经验。",
        encoding="utf-8",
    )
    (methodology / "编程之道.md").write_text(
        "# 编程之道\n\n编程哲学与思维方式。",
        encoding="utf-8",
    )

    templates = zh_docs / "Templates and Resources"
    templates.mkdir(parents=True)
    (templates / "通用项目架构模板.md").write_text(
        "# 通用项目架构模板\n\n适用于各类项目的架构设计模板。",
        encoding="utf-8",
    )

    tutorials = zh_docs / "Tutorials and Guides"
    tutorials.mkdir(parents=True)
    (tutorials / "快速入门.md").write_text(
        "# 快速入门\n\n新手入门教程。",
        encoding="utf-8",
    )

    return tmp_path
