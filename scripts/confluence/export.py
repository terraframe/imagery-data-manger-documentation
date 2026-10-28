"""Export a Confluence page tree (storage-format bodies + attachments) to disk.

Usage:
    python3 scripts/confluence/export.py [--root PAGE_ID] [--out DIR]

Writes:
    DIR/tree.json                  page metadata in depth-first order
    DIR/pages/<id>.xml             storage-format body of each page
    DIR/attachments/<id>/<file>    every attachment on each page

Only works for spaces that allow anonymous read access.
"""
import argparse
import json
import os
import urllib.request

BASE = "https://terraframe.atlassian.net/wiki"
API = BASE + "/rest/api/content/"
DEFAULT_ROOT = "921075893"  # OSMRE "Public Documentation"


def get_json(url):
    with urllib.request.urlopen(url) as r:
        return json.load(r)


def paged(url):
    """Yield every result from a paged Confluence REST collection."""
    start = 0
    while True:
        sep = "&" if "?" in url else "?"
        page = get_json(f"{url}{sep}limit=100&start={start}")
        yield from page["results"]
        if page["size"] < 100:
            return
        start += 100


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        f.write(r.read())


def export_page(page_id, depth, parent, out, tree):
    page = get_json(API + page_id + "?expand=body.storage,version")
    with open(os.path.join(out, "pages", page_id + ".xml"), "w") as f:
        f.write(page["body"]["storage"]["value"])

    attachments = []
    for att in paged(API + page_id + "/child/attachment"):
        name = att["title"]
        download(BASE + att["_links"]["download"], os.path.join(out, "attachments", page_id, name))
        attachments.append(name)

    tree.append({
        "id": page_id,
        "title": page["title"],
        "depth": depth,
        "parent": parent,
        "updated": page["version"]["when"],
        "url": BASE + page["_links"]["webui"],
        "attachments": attachments,
    })
    print("  " * depth + f"- {page['title']} ({len(attachments)} attachments)")

    for child in paged(API + page_id + "/child/page?expand=extensions.position"):
        export_page(child["id"], depth + 1, page_id, out, tree)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--out", default=".confluence-export")
    args = parser.parse_args()

    os.makedirs(os.path.join(args.out, "pages"), exist_ok=True)
    tree = []
    export_page(args.root, 0, None, args.out, tree)
    with open(os.path.join(args.out, "tree.json"), "w") as f:
        json.dump(tree, f, indent=1)


if __name__ == "__main__":
    main()
