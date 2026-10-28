import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

type Props = {
  // Key of `customFields.deployment` in docusaurus.config.ts
  value: string;
  // Render URLs as plain text instead of a link
  plain?: boolean;
  // Appended to the value, e.g. a page path within the IDM application
  path?: string;
};

// Renders a deployment-specific value (e.g. the IDM application URL) so the
// docs can be reused by other IDM deployments by changing only the config.
export default function Deployment({value, plain, path}: Props): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  const values = siteConfig.customFields?.deployment as Record<string, string>;
  const base = values?.[value];
  if (base === undefined) {
    throw new Error(`Unknown deployment value "${value}"`);
  }
  const text = path ? base + path : base;
  if (!plain && /^https?:\/\//.test(text)) {
    return <a href={text}>{text}</a>;
  }
  return text;
}
