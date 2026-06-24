import os
import re


TYPE_MAP = {
    "Methodology and Principles": "methodology",
    "Templates and Resources": "template",
    "Tutorials and Guides": "tutorial",
}


class DocLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.docs: dict[str, dict] = {}

    def scan(self):
        self.docs.clear()
        for lang in self.languages:
            docs_dir = os.path.join(self.resource_path, "i18n", lang, "documents")
            if not os.path.isdir(docs_dir):
                continue
            for type_dir in os.listdir(docs_dir):
                type_path = os.path.join(docs_dir, type_dir)
                if not os.path.isdir(type_path):
                    continue
                doc_type = TYPE_MAP.get(type_dir, "other")
                for fname in os.listdir(type_path):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(type_path, fname)
                    self._index_file(fpath, doc_type, lang)

    def _index_file(self, fpath: str, doc_type: str, language: str):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title = self._extract_title(content, fpath)
        summary = self._extract_summary(content, max_length=500)
        tags = self._extract_tags(fpath, doc_type)

        file_id = f"{doc_type}_{language}_{os.path.basename(fpath)}"
        self.docs[file_id] = {
            "id": file_id,
            "title": title,
            "path": fpath,
            "type": doc_type,
            "language": language,
            "tags": tags,
            "summary": summary,
            "content": content,
            "size": len(content.encode("utf-8")),
        }

    def search(self, topic: str, doc_type: str = "all", limit: int = 10) -> list[dict]:
        topic_lower = topic.lower()
        results = []
        for entry in self.docs.values():
            if doc_type != "all" and entry["type"] != doc_type:
                continue
            score = 0
            if topic_lower in entry["title"].lower():
                score += 3
            if any(topic_lower in tag.lower() for tag in entry["tags"]):
                score += 2
            if topic_lower in entry["summary"].lower():
                score += 1
            if topic_lower in entry["content"].lower():
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
    def _extract_tags(fpath: str, doc_type: str) -> list[str]:
        tags = []
        type_labels = {
            "methodology": "方法论",
            "template": "模板",
            "tutorial": "教程",
        }
        if doc_type in type_labels:
            tags.append(type_labels[doc_type])
        basename = os.path.basename(fpath).replace(".md", "")
        parts = basename.replace("_", " ").split()
        tags.extend(p for p in parts if len(p) > 1)
        return tags
