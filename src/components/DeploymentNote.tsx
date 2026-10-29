import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Admonition from '@theme/Admonition';

type Props = {
  // Key of `customFields.deployment` in docusaurus.config.ts
  value: string;
};

// Tells readers on other IDM installations which part of an address shown on
// the page is specific to this deployment, and what to replace it with.
export default function DeploymentNote({value}: Props): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  const values = siteConfig.customFields?.deployment as Record<string, string>;
  const text = values?.[value];
  if (text === undefined) {
    throw new Error(`Unknown deployment value "${value}"`);
  }
  return (
    <Admonition type="note" title="Other installations">
      <p>
        Addresses on this page are for the {values.name} installation of IDM. On
        other installations of IDM, replace <code>{text}</code> with your
        installation's address.
      </p>
    </Admonition>
  );
}
