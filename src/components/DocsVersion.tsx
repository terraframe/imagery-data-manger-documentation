import type {ReactNode} from 'react';
import {useDocsVersion} from '@docusaurus/plugin-content-docs/client';

// Renders the label of the docs version being viewed (e.g. "1.8.x"), so pages
// never hard code the IDM release they document.
export default function DocsVersion(): ReactNode {
  return useDocsVersion().label;
}
