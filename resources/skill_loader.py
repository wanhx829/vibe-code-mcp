import os
import re


class SkillLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.skills: dict[str, dict] = {}

    def scan(self):
        self.skills.clear()
        for lang in self.languages:
            skills_dir = os.path.join(self.resource_path, "i18n", lang, "skills")
            if not os.path.isdir(skills_dir):
                continue
            for entry in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, entry)
                if not os.path.isdir(skill_path):
                    continue
                skill_md = os.path.join(skill_path, "SKILL.md")
                if not os.path.isfile(skill_md):
                    continue
                self._index_skill(skill_md, entry, lang)

    def _index_skill(self, skill_md: str, skill_name: str, language: str):
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title, description = self._parse_frontmatter(content, skill_name)
        references = self._scan_references(os.path.dirname(skill_md))

        self.skills[skill_name] = {
            "id": skill_name,
            "title": title,
            "path": skill_md,
            "domain": description,
            "language": language,
            "size": len(content.encode("utf-8")),
            "content": content,
            "references": references,
        }

    def search(self, keyword: str, limit: int = 10) -> list[dict]:
        keyword_lower = keyword.lower()
        results = []
        for entry in self.skills.values():
            score = 0
            if keyword_lower in entry["id"].lower():
                score += 3
            if keyword_lower in entry["title"].lower():
                score += 3
            if keyword_lower in entry["domain"].lower():
                score += 2
            if keyword_lower in entry["content"].lower():
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]

    @staticmethod
    def _parse_frontmatter(content: str, fallback_name: str) -> tuple[str, str]:
        title = fallback_name
        description = ""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                for line in fm.strip().split("\n"):
                    if line.startswith("name:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("description:"):
                        description = line.split(":", 1)[1].strip().strip('"')
        if not title:
            title = fallback_name
        return title, description

    @staticmethod
    def _scan_references(skill_dir: str) -> list[dict]:
        refs = []
        ref_dir = os.path.join(skill_dir, "references")
        if not os.path.isdir(ref_dir):
            return refs
        for fname in os.listdir(ref_dir):
            if fname.endswith(".md"):
                refs.append({
                    "title": fname.replace(".md", ""),
                    "path": os.path.join(ref_dir, fname),
                })
        return refs
