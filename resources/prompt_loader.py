import os
import re


CATEGORY_MAP = {
    "coding_prompts": "coding",
    "system_prompts": "system",
    "user_prompts": "user",
    "meta_prompts": "meta",
}


class PromptLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None, include_prompt_docs: bool = True):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.include_prompt_docs = include_prompt_docs
        self.prompts: dict[str, dict] = {}

    def scan(self):
        self.prompts.clear()
        for lang in self.languages:
            prompts_dir = os.path.join(self.resource_path, "i18n", lang, "prompts")
            if not os.path.isdir(prompts_dir):
                continue
            for category_dir in os.listdir(prompts_dir):
                category_path = os.path.join(prompts_dir, category_dir)
                if not os.path.isdir(category_path):
                    continue
                category = CATEGORY_MAP.get(category_dir, category_dir)
                for fname in os.listdir(category_path):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(category_path, fname)
                    self._index_file(fpath, category, lang)

        if self.include_prompt_docs:
            self._scan_prompt_docs()

    def _scan_prompt_docs(self):
        prompt_docs_dir = os.path.join(
            self.resource_path, "libs", "external", "prompts-library", "prompt_docs"
        )
        if not os.path.isdir(prompt_docs_dir):
            return
        for root, _dirs, files in os.walk(prompt_docs_dir):
            for fname in files:
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(root, fname)
                self._index_file(fpath, "prompt_docs", "mixed")

    def _index_file(self, fpath: str, category: str, language: str):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title = self._extract_title(content, fpath)
        summary = self._extract_summary(content, max_length=500)
        tags = self._extract_tags(fpath, category)

        file_id = f"{category}_{language}_{os.path.basename(fpath)}"
        self.prompts[file_id] = {
            "id": file_id,
            "title": title,
            "path": fpath,
            "category": category,
            "language": language,
            "tags": tags,
            "summary": summary,
            "content": content,
            "size": len(content.encode("utf-8")),
        }

    def search(self, query: str, category: str = "all", limit: int = 10) -> list[dict]:
        query_lower = query.lower()
        results = []
        for entry in self.prompts.values():
            if category != "all" and entry["category"] != category:
                continue
            score = 0
            if query_lower in entry["title"].lower():
                score += 3
            if any(query_lower in tag.lower() for tag in entry["tags"]):
                score += 2
            if query_lower in entry["summary"].lower():
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]

    @staticmethod
    def _extract_title(content: str, fpath: str) -> str:
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        basename = os.path.basename(fpath)
        return re.sub(r"^\(\d+,\d+\)_", "", basename).replace(".md", "").replace("_", " ").strip()

    @staticmethod
    def _extract_summary(content: str, max_length: int = 500) -> str:
        text = content.lstrip()
        if text.startswith("---"):
            parts = text.split("---", 2)
            text = parts[2].lstrip() if len(parts) >= 3 else text
        text = text[:max_length]
        last_period = max(text.rfind("。"), text.rfind(". "), text.rfind("\n"))
        if last_period > 50:
            text = text[:last_period + 1]
        return text.strip()

    @staticmethod
    def _extract_tags(fpath: str, category: str) -> list[str]:
        tags = []
        category_labels = {
            "coding": "编程",
            "system": "系统",
            "user": "用户",
            "meta": "元提示词",
        }
        if category in category_labels:
            tags.append(category_labels[category])
        basename = os.path.basename(fpath)
        name = re.sub(r"^\(\d+,\d+\)_", "", basename).replace(".md", "")
        parts = re.split(r"[_\s]+", name)
        tags.extend(p for p in parts if len(p) > 1)
        return tags
