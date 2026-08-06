/**
 * Shared Company Configuration
 * Single source of truth for all schema defaults
 */

export const COMPANY = {
  name: 'Monsoft Solutions',
  url: 'https://monsoftsolutions.com',
  logo: 'https://monsoftsolutions.com/logo.svg',
  email: 'hello@monsoftsolutions.com',
  description:
    'AI-first software company building intelligent solutions that transform how businesses operate.',
  address: {
    addressLocality: 'Miami',
    addressRegion: 'FL',
    addressCountry: 'US',
  },
  sameAs: [
    'https://linkedin.com/company/monsoft-solutions',
    'https://github.com/Monsoft-Solutions',
  ],
  areaServed: ['United States', 'Worldwide'],
  // Default image for LocalBusiness schema
  image: 'https://monsoftsolutions.com/og-image.jpg',
} as const;

/**
 * Schema IDs for @id linking between schemas
 * Using hash fragments as recommended by Google
 */
export const SCHEMA_IDS = {
  organization: `${COMPANY.url}/#organization`,
  website: `${COMPANY.url}/#website`,
  localBusiness: `${COMPANY.url}/#localbusiness`,
} as const;

/**
 * Base URL for constructing absolute URLs
 */
export const BASE_URL = COMPANY.url;
