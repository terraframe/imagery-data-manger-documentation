import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'IDM Documentation',
  tagline: 'Imagery Data Management platform documentation',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://terraframe.github.io',
  baseUrl: '/imagery-data-manger-documentation/',
  organizationName: 'terraframe',
  projectName: 'imagery-data-manger-documentation',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
      onBrokenMarkdownImages: 'throw',
    },
  },

  // Values that differ between IDM deployments. Use them in docs with
  // <Deployment value="appUrl" /> instead of hard coding them.
  customFields: {
    deployment: {
      appUrl: 'https://aim.geoplatform.gov/',
      knowStacUrl: 'https://knowstac.geoprism.net/dev/',
      publicBucketUrl: 'https://osmre-uas-prod-public.s3.amazonaws.com',
    },
  },

  // Roboto is the IDM app's font.
  stylesheets: [
    'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap',
  ],

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/terraframe/imagery-data-manger-documentation/tree/main/',
          // docs/ is the current IDM release. See README.md for cutting a new version.
          lastVersion: 'current',
          versions: {
            current: {
              label: '1.8.x',
              path: '',
            },
          },
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Imagery Data Manager (IDM) Documentation',
      items: [
        {
          type: 'docsVersionDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/terraframe/imagery-data-manger-documentation',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Getting Started', to: '/getting-started/accessing-idm'},
            {label: 'Field Worker Guides', to: '/field-worker'},
            {label: 'Administrator Guide', to: '/administration'},
          ],
        },
        {
          title: 'More',
          items: [
            {label: 'Know-STAC', to: '/know-stac'},
            {label: 'FAQ', to: '/faq'},
            {label: 'GitHub', href: 'https://github.com/terraframe/imagery-data-manger-documentation'},
          ],
        },
      ],
      copyright: 'Documentation dedicated to the public domain under <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0 Universal</a>.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
