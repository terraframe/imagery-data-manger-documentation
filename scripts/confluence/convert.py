"""Convert exported Confluence storage-format pages to Docusaurus-flavored Markdown.

Usage:
    python3 scripts/confluence/convert.py [--export DIR]

Reads DIR/pages/<id>.xml and writes DIR/md/<id>.md. Requires beautifulsoup4.

Conventions in the output (resolved later by assemble.py):
    ![alt](img/<slug>)              image attachment of the same page
    [text](confluence:<id>#anchor)  link to another Confluence page
"""
import argparse
import json
import os
import re

from bs4 import BeautifulSoup, NavigableString, Tag

ADMONITIONS = {"info": "info", "note": "warning", "warning": "danger", "tip": "tip", "success": "tip", "error": "danger"}
SKIPPED_MACROS = {"toc", "style", "anchor"}
PAGE_URL = re.compile(r"atlassian\.net/wiki/spaces/[^/]+/pages/(\d+)[^#]*(#.*)?")


def slug_filename(name):
    base, ext = os.path.splitext(name)
    base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return base + ext.lower()


def anchor(text):
    """Confluence heading anchor ("Supported File Formats" -> "Supported-File-Formats")."""
    return text.strip().replace(" ", "-")


class Converter:
    def __init__(self, titles):
        self.titles = titles  # page title -> page id

    # ---- inline -------------------------------------------------------

    def inline(self, node):
        if isinstance(node, NavigableString):
            if node.__class__.__name__ in ("Comment", "Doctype"):
                return ""
            text = str(node).replace("\xa0", " ")
            text = re.sub(r"\s+", " ", text)
            return text.replace("{", "\\{").replace("}", "\\}").replace("<", "&lt;").replace(">", "&gt;")
        name = node.name
        if name in ("strong", "b"):
            return self.wrap("**", self.inlines(node))
        if name in ("em", "i"):
            return self.wrap("*", self.inlines(node))
        if name in ("s", "del"):
            return self.wrap("~~", self.inlines(node))
        if name == "code":
            return "`" + node.get_text().replace("`", "'") + "`"
        if name == "br":
            return "<br />"
        if name == "ac:image":
            return self.image(node)
        if name == "a":
            return self.link(node.get("href", ""), self.inlines(node))
        if name == "ac:link":
            return self.page_link(node)
        if name == "ac:structured-macro" and node.get("ac:name") in SKIPPED_MACROS:
            return ""
        if name in ("ac:parameter", "ac:caption"):
            return ""
        return self.inlines(node)

    def inlines(self, node):
        return "".join(self.inline(c) for c in node.children)

    @staticmethod
    def wrap(mark, text):
        if not text.strip():
            return text
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        return f"{lead}{mark}{text.strip()}{mark}{trail}"

    def image(self, node):
        att = node.find("ri:attachment")
        if att is not None:
            return f"![](img/{slug_filename(att['ri:filename'])})"
        url = node.find("ri:url")
        return f"![]({url['ri:value']})" if url is not None else ""

    def link(self, href, text):
        m = PAGE_URL.search(href)
        if m:
            href = f"confluence:{m.group(1)}{m.group(2) or ''}"
        text = text.strip() or href
        return f"[{text}]({href})"

    def page_link(self, node):
        page = node.find("ri:page")
        body = node.find("ac:link-body") or node.find("ac:plain-text-link-body")
        text = self.inlines(body).strip() if body else ""
        target = ""
        if page is not None:
            title = page.get("ri:content-title", "")
            target = f"confluence:{self.titles.get(title, title)}"
            text = text or title
        if node.get("ac:anchor"):
            target += "#" + node["ac:anchor"]
        return f"[{text}]({target})"

    # ---- blocks -------------------------------------------------------

    def blocks(self, node):
        """Render children of node as a list of Markdown blocks."""
        out, run = [], []

        def flush():
            text = "".join(run).strip()
            if text:
                out.append(text)
            run.clear()

        for child in node.children:
            if isinstance(child, Tag) and self.is_block(child):
                flush()
                out.extend(b for b in self.block(child) if b.strip())
            else:
                run.append(self.inline(child))
        flush()
        return out

    def is_block(self, node):
        if node.name == "ac:structured-macro":
            return node.get("ac:name") not in SKIPPED_MACROS
        return node.name in {
            "p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table", "blockquote",
            "hr", "pre", "ac:adf-extension", "ac:layout", "ac:layout-section", "ac:layout-cell",
        }

    def block(self, node):
        name = node.name
        if name == "p":
            text = self.inlines(node).strip()
            return [text] if text else []
        if re.fullmatch(r"h[1-6]", name):
            text = self.inlines(node).strip()
            return [f"{'#' * int(name[1])} {text}"] if text else []
        if name in ("ul", "ol"):
            return [self.list_(node)]
        if name == "table":
            return [self.table(node)]
        if name == "blockquote":
            return ["\n".join("> " + line for line in "\n\n".join(self.blocks(node)).splitlines())]
        if name == "hr":
            return ["---"]
        if name == "pre":
            return [f"```\n{node.get_text()}\n```"]
        if name == "ac:structured-macro":
            return self.macro(node)
        if name == "ac:adf-extension":
            panel = node.find("ac:adf-node")
            kind = panel.find("ac:adf-attribute", key="panel-type") if panel else None
            content = node.find("ac:adf-content")
            return [self.admonition(kind.get_text() if kind else "note", "", self.blocks(content))]
        return self.blocks(node)  # div, layouts

    def macro(self, node):
        name = node.get("ac:name")
        params = {p.get("ac:name"): p.get_text() for p in node.find_all("ac:parameter", recursive=False)}
        if name == "code":
            body = node.find("ac:plain-text-body")
            lang = params.get("language", "")
            return [f"```{lang}\n{body.get_text().strip(chr(10)) if body else ''}\n```"]
        body = node.find("ac:rich-text-body", recursive=False)
        content = self.blocks(body) if body else []
        if name in ADMONITIONS:
            return [self.admonition(name, params.get("title", ""), content)]
        return content

    @staticmethod
    def admonition(kind, title, content):
        kind = ADMONITIONS.get(kind, "note")
        head = f":::{kind}[{title}]" if title else f":::{kind}"
        return head + "\n\n" + "\n\n".join(content) + "\n\n:::"

    def list_(self, node, depth=0):
        lines = []
        ordered = node.name == "ol"
        for i, li in enumerate(node.find_all("li", recursive=False), 1):
            marker = f"{i}. " if ordered else "- "
            pad = " " * len(marker)
            parts = []
            for b in self.blocks(li):
                parts.append(b)
            text = "\n\n".join(parts) if parts else ""
            body = text.splitlines() or [""]
            lines.append(marker + body[0])
            lines.extend((pad + l) if l.strip() else "" for l in body[1:])
        return "\n".join(lines)

    def table(self, node):
        rows = []
        for tr in node.find_all("tr"):
            if tr.find_parent("table") is not node:
                continue
            cells = tr.find_all(["th", "td"], recursive=False)
            rows.append(([self.cell(c) for c in cells], all(c.name == "th" for c in cells)))
        if not rows:
            return ""
        width = max(len(r) for r, _ in rows)
        rows = [(r + [""] * (width - len(r)), h) for r, h in rows]
        header, body = (rows[0][0], rows[1:]) if rows[0][1] else ([""] * width, rows)
        lines = ["| " + " | ".join(header) + " |", "|" + "---|" * width]
        lines += ["| " + " | ".join(r) + " |" for r, _ in body]
        return "\n".join(lines)

    def cell(self, node):
        parts = []
        for b in self.blocks(node):
            if b.startswith(":::"):  # admonitions can't live in a table cell
                b = "\n".join(l for l in b.splitlines() if not l.startswith(":::"))
            parts.append(b)
        text = "<br /><br />".join(p.strip() for p in parts if p.strip())
        text = re.sub(r"\n+(?=[-\d])", "<br />", text)  # list items
        text = re.sub(r"\s*\n\s*", " ", text)
        return text.replace("|", "\\|")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--export", default=".confluence-export")
    args = parser.parse_args()

    with open(os.path.join(args.export, "tree.json")) as f:
        tree = json.load(f)
    converter = Converter({p["title"]: p["id"] for p in tree})
    os.makedirs(os.path.join(args.export, "md"), exist_ok=True)
    for page in tree:
        with open(os.path.join(args.export, "pages", page["id"] + ".xml")) as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        md = "\n\n".join(converter.blocks(soup)) + "\n"
        with open(os.path.join(args.export, "md", page["id"] + ".md"), "w") as f:
            f.write(md)
        print(f"{page['id']}  {page['title']}")


if __name__ == "__main__":
    main()
