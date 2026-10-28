"""Assemble converted Confluence Markdown into the Docusaurus docs/ tree.

Usage:
    python3 scripts/confluence/assemble.py [--export DIR] [--docs DIR]

This was a one-time migration step. The generated pages were edited by hand
afterwards, so re-running it will overwrite those edits.

The MANIFEST below maps sections of the original Confluence pages (by heading)
onto new doc files. For each doc it:
  - normalizes heading levels so the doc's sections start at h2
  - copies the images it references into an img/ folder next to the doc
  - rewrites links to other Confluence pages as relative file links
"""
import argparse
import json
import os
import re
import shutil

from convert import slug_filename

# Confluence page ids
ROOT, FEATURES, WORKFLOWS = "921075893", "922353685", "923303937"
ADMIN, FAQ, KNOWSTAC = "921567417", "2464153795", "3761471489"


def S(page, heading=None, keep=False, intro=False):
    """A section of a converted page: the content under `heading` (or the whole
    page if None). keep=True keeps the heading itself; intro=True stops at the
    first sub-heading."""
    return (page, heading, keep, intro)


def doc(title, position, *sections, slug=None):
    return {"title": title, "position": position, "sections": sections, "slug": slug}


MANIFEST = {
    "intro.md": doc("Introduction", 1, S(FEATURES, "About the Application"), S(ROOT, "Application URL", True),
                    S(ROOT, "Application Version Info", True), slug="/"),

    "getting-started/accessing-idm.md": doc("Accessing IDM", 1, S(WORKFLOWS, "Accessing IDM")),
    "getting-started/tour-of-idm.md": doc(
        "Tour of IDM", 2, S(FEATURES, "Site Viewer", intro=True), S(FEATURES, "IDM Sites", True),
        S(FEATURES, "Lefthand Navigation Panels of the Hierarchy", True)),
    "getting-started/data-hierarchy.md": doc("Data Hierarchy", 3, S(WORKFLOWS, "IDM Data Hierarchy Deep Dive")),

    "field-worker/organizing-data/sites.md": doc("Sites", 1, S(WORKFLOWS, "Add a New Site", True)),
    "field-worker/organizing-data/projects.md": doc("Projects", 2, S(WORKFLOWS, "Create a Project", True)),
    "field-worker/organizing-data/missions.md": doc("Missions", 3, S(WORKFLOWS, "Create a Mission", True)),
    "field-worker/organizing-data/collections.md": doc(
        "Collections", 4, S(WORKFLOWS, "Create a Collection", True), S(FEATURES, "Collection Data and Management", True)),
    "field-worker/organizing-data/private-collections.md": doc(
        "Private Collections", 5, S(WORKFLOWS, "Managing Private Collections")),

    "field-worker/uploading-data/index.md": doc(
        "Uploading Data", 2, S(WORKFLOWS, "Upload Data to the Raw Directory of a Collection", intro=True),
        S(WORKFLOWS, "Supported File Formats", True), S(WORKFLOWS, "Best Practices", True), S(WORKFLOWS, "Next Steps", True)),
    "field-worker/uploading-data/still-imagery.md": doc("Still Imagery", 1, S(WORKFLOWS, "Upload Still Imagery")),
    "field-worker/uploading-data/multispectral-imagery.md": doc(
        "Multispectral Imagery", 2, S(WORKFLOWS, "Upload Multispectral Imagery")),
    "field-worker/uploading-data/video.md": doc("Video", 3, S(WORKFLOWS, "Upload Video")),
    "field-worker/uploading-data/lidar.md": doc("LiDAR", 4, S(WORKFLOWS, "Upload LiDAR")),

    "field-worker/workflow-tasks.md": doc(
        "Workflow Tasks", 3, S(WORKFLOWS, "Monitoring and Managing Workflow Tasks", intro=True), S(FEATURES, "Workflow Tasks", True)),

    "field-worker/products/index.md": doc("Working With Products", 4, S(WORKFLOWS, "Working With Products", intro=True)),
    "field-worker/products/generating-products.md": doc(
        "Generating Products", 1, S(WORKFLOWS, "Derive Products from Still Imagery, Thermal Imagery, Multispectral Imagery, or Video")),
    "field-worker/products/geologger.md": doc("Geologger Files", 2, S(WORKFLOWS, "Geologger Workflow")),
    "field-worker/products/ground-control-points.md": doc(
        "Ground Control Points", 3, S(WORKFLOWS, "Ground Control Point (GCP) Workflow")),
    "field-worker/products/uploading-products.md": doc("Uploading Products", 4, S(WORKFLOWS, "Manually Uploading Products")),
    "field-worker/products/viewing-products.md": doc(
        "Viewing Products", 5, S(WORKFLOWS, "Viewing Generated Products in a Collection", True),
        S(WORKFLOWS, "Viewing Generated Products in the Products Tab", True), S(FEATURES, "Products in the Hierarchy", True)),

    "field-worker/publishing-products.md": doc("Publishing Products", 5, S(WORKFLOWS, "Sharing Products")),
    "field-worker/image-sets.md": doc("Image Sets", 6, S(WORKFLOWS, "Working With Image Sets")),
    "field-worker/downloading-files.md": doc("Downloading Files", 7, S(WORKFLOWS, "Downloading Files")),

    "administration/index.md": doc("Administrator Guide", 4, S(ADMIN, "About Administration Of IDM")),
    "administration/accounts.md": doc("Accounts", 1, S("2377285735")),
    "administration/platforms-and-sensors.md": doc("Platforms and Sensors", 2, S("2377154725")),
    "administration/uav-registration.md": doc("UAV Registration", 3, S("3204120578")),
    "administration/organizations.md": doc("Organizations", 4, S("3204153347")),
    "administration/custom-hierarchies.md": doc("Custom Hierarchies", 5, S("3236495361")),
    "administration/public-image-services.md": doc("Public Image Services", 6, S("2468052997")),
    "administration/reporting.md": doc("Reporting", 7, S("3204055043")),
    "administration/email-settings.md": doc("Email Settings", 8, S("2464022682")),
    "administration/icons.md": doc("Icons", 9, S("2464055402")),
    "administration/session-event-log.md": doc("Session Event Log", 10, S("2464088231")),

    "know-stac.md": doc("Know-STAC", 5, S(KNOWSTAC)),
    "faq.md": doc("Frequently Asked Questions", 6, S(FAQ)),
}

# Confluence link targets ("<page id>" or "<page id>#<anchor>") -> doc path
LINKS = {
    WORKFLOWS + "#Supported-File-Formats": "field-worker/uploading-data/index.md#supported-file-formats",
    WORKFLOWS + "#Create-a-Collection": "field-worker/organizing-data/collections.md",
    WORKFLOWS + "#Geologger-Workflow": "field-worker/products/geologger.md",
    WORKFLOWS + "#Ground-Control-Point-(GCP)-Workflow": "field-worker/products/ground-control-points.md",
    WORKFLOWS + "#Monitoring-and-Managing-Workflow-Tasks": "field-worker/workflow-tasks.md",
    "2377220169": "field-worker/index.md",
    "2377154725": "administration/platforms-and-sensors.md",
    ADMIN: "administration/index.md",
    KNOWSTAC: "know-stac.md",
    FAQ: "faq.md",
}

HEADING = re.compile(r"^(#{1,6}) (.*)$")


def section(lines, heading, keep, intro):
    """Return the lines of a heading's section, or the whole page if heading is None."""
    if heading is None:
        return lines
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m and m.group(2).strip() == heading:
            level = len(m.group(1))
            end = next((j for j in range(i + 1, len(lines))
                        if (h := HEADING.match(lines[j])) and (intro or len(h.group(1)) <= level)), len(lines))
            return lines[i if keep else i + 1:end]
    raise KeyError(f"heading not found: {heading!r}")


def normalize_headings(lines):
    """Map the distinct heading levels in a block onto h2, h3, ... in order."""
    levels = sorted({len(m.group(1)) for l in lines if (m := HEADING.match(l))})
    mapping = {lvl: min(i + 2, 6) for i, lvl in enumerate(levels)}
    out = []
    for line in lines:
        m = HEADING.match(line)
        out.append(f"{'#' * mapping[len(m.group(1))]} {m.group(2).strip()}" if m else line)
    return out


def rewrite_links(text, path, titles):
    def repl(m):
        label, target = m.group(1), m.group(2)
        key = target[len("confluence:"):]
        dest = LINKS.get(key) or LINKS.get(key.split("#")[0])
        if dest is None:
            print(f"  unresolved link in {path}: {target}")
            return m.group(0)
        file, _, frag = dest.partition("#")
        rel = os.path.relpath(file, os.path.dirname(path) or ".")
        if label.startswith("http"):  # Confluence page cards render as bare URLs
            label = titles[file]
        return f"[{label}]({rel}{'#' + frag if frag else ''})"
    # targets may contain one level of parentheses, e.g. "#Ground-Control-Point-(GCP)-Workflow"
    return re.sub(r"\[([^\]]*)\]\((confluence:(?:[^()\s]|\([^()\s]*\))+)\)", repl, text)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--export", default=".confluence-export")
    parser.add_argument("--docs", default="docs")
    args = parser.parse_args()

    with open(os.path.join(args.export, "tree.json")) as f:
        tree = {p["id"]: p for p in json.load(f)}
    pages = {}
    for pid in tree:
        with open(os.path.join(args.export, "md", pid + ".md")) as f:
            pages[pid] = f.read().splitlines()
    attachments = {pid: {slug_filename(a): a for a in p["attachments"]} for pid, p in tree.items()}
    titles = {path: d["title"] for path, d in MANIFEST.items()}

    for path, d in MANIFEST.items():
        body = []
        for page, heading, keep, intro in d["sections"]:
            lines = section(pages[page], heading, keep, intro)
            block = "\n".join(normalize_headings(lines)).strip()
            # copy referenced images next to the doc
            for name in re.findall(r"\]\(img/([^)]+)\)", block):
                src = os.path.join(args.export, "attachments", page, attachments[page][name])
                dest = os.path.join(args.docs, os.path.dirname(path), "img", name)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(src, dest)
            body.append(block)

        text = "\n\n".join(b for b in body if b)
        text = re.sub(r" ?<br />$", "", text, flags=re.M)
        text = rewrite_links(text, path, titles)
        front = ["---", f"title: {d['title']}", f"sidebar_position: {d['position']}"]
        if d["slug"]:
            front.append(f"slug: {d['slug']}")
        front.append("---")

        dest = os.path.join(args.docs, path)
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w") as f:
            f.write("\n".join(front) + "\n\n" + text + "\n")
        print(path)


if __name__ == "__main__":
    main()
