# IDM Documentation

Documentation for the Imagery Data Manager (IDM) platform, built with [Docusaurus](https://docusaurus.io/) and published to GitHub Pages at https://terraframe.github.io/imagery-data-manger-documentation/.

## Local Development

Requires Node.js 20 or newer (see `.nvmrc`).

```bash
npm install
npm start
```

This starts a local development server with live reload. To check a production build (which fails on broken links and images):

```bash
npm run build
npm run serve
```

Search is only available in the production build.

To add or upgrade a package, use npm 11 (`npx npm@11 install <package>`). npm 10.9 hangs while resolving the dependency tree of `@easyops-cn/docusaurus-search-local`. Installing from the existing lock file (`npm install` or `npm ci`) works with either version.

## Writing Docs

- Pages live in `docs/`. The sidebar is generated from the folder structure. Order pages with `sidebar_position` front matter and folders with `_category_.json`.
- Put screenshots in an `img/` folder next to the page that uses them and reference them with a relative path (`![](img/screenshot.png)`). Keeping images next to the docs means each version snapshot keeps its own screenshots.
- Link to other pages by relative file path (`[Collections](../organizing-data/collections.md)`), not by URL. File links keep working across versions.
- Reusable snippets are Markdown files whose names start with `_` (for example `docs/field-worker/uploading-data/_zip-requirements.md`). They aren't pages on their own and are imported where needed.

### Deployment-specific values

Values that differ between IDM deployments, such as the application URL, are set in `customFields.deployment` in `docusaurus.config.ts`. Use them in docs with the `Deployment` component instead of hard coding them:

```md
You can access the application at <Deployment value="appUrl" />.

<DeploymentNote value="appUrl" />
```

`DeploymentNote` adds an "Other installations" note telling readers on other IDM installations which part of the address to replace. Add one to any page that shows a deployment-specific address. `name` is the installation name used in that note (for example `DOI GeoPlatform`).

To build the docs for a different IDM deployment, change those values.

## Versions

`docs/` always documents the current IDM release. Its version label is set in `docusaurus.config.ts` (`versions.current.label`). Use `<DocsVersion />` in a page to show that label instead of typing the version.

When a new IDM release is made, snapshot the docs for the release that's ending **before** updating them for the new one:

```bash
# Freeze the current docs as 1.8 (copies docs/ to versioned_docs/version-1.8/)
npm run docusaurus docs:version 1.8
```

Then update `versions.current.label` in `docusaurus.config.ts` to the new release (for example `1.9.x`) and update `docs/` as features change. Older versions appear in the version dropdown and are served under their version path (for example `/1.8/`).

Versioned docs are frozen copies. Only edit them to fix errors that apply to that release.

## Deployment

Pushing to `main` runs the [Build and deploy](.github/workflows/deploy.yml) workflow, which builds the site and publishes it to the `gh-pages` branch. Pull requests run the build to catch broken links and images.

GitHub Pages must be set to deploy from the `gh-pages` branch (Settings → Pages → Build and deployment → Deploy from a branch).

## Confluence Migration

These docs were migrated from the [OSMRE Public Documentation](https://terraframe.atlassian.net/wiki/spaces/OSMRE/pages/921075893/Public+Documentation) Confluence space using the scripts in `scripts/confluence/` (requires Python 3 with `beautifulsoup4`):

1. `export.py` downloads the page tree and attachments to `.confluence-export/`.
2. `convert.py` converts the Confluence storage format to Markdown.
3. `assemble.py` splits and merges the converted pages into `docs/` using the mapping in its `MANIFEST`.

The generated pages were edited by hand after the migration, so don't re-run `assemble.py` over `docs/`.

## License

This documentation is dedicated to the public domain under [CC0 1.0 Universal](LICENSE).
Code samples in this documentation are licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0), matching the [IDM source code](https://github.com/terraframe/osmre-uav).
