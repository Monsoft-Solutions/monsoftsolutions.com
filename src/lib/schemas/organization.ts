/**
 * Organization Schema Builder
 * Creates schema.org Organization structured data
 */

import type { OrganizationSchema, PostalAddress, ContactPoint, ImageObject } from './types';

export interface OrganizationConfig {
  name?: string;
  url?: string;
  logo?: string;
  description?: string;
  foundingDate?: string;
  address?: Partial<PostalAddress>;
  contactPoint?: ContactPoint | ContactPoint[];
  sameAs?: string[];
  email?: string;
  telephone?: string;
}

// Default organization data for Monsoft Solutions
const defaults: Required<
  Pick<OrganizationConfig, 'name' | 'url' | 'logo' | 'description' | 'address' | 'sameAs'>
> = {
  name: 'Monsoft Solutions',
  url: 'https://monsoftsolutions.com',
  logo: 'https://monsoftsolutions.com/logo.svg',
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
};

/**
 * Creates an Organization schema with sensible defaults for Monsoft Solutions
 */
export function createOrganizationSchema(config: OrganizationConfig = {}): OrganizationSchema {
  const mergedConfig = { ...defaults, ...config };

  const schema: OrganizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: mergedConfig.name,
    url: mergedConfig.url,
    logo: mergedConfig.logo,
    description: mergedConfig.description,
  };

  // Add optional address
  if (mergedConfig.address) {
    schema.address = {
      '@type': 'PostalAddress',
      ...mergedConfig.address,
    };
  }

  // Add social profiles
  if (mergedConfig.sameAs && mergedConfig.sameAs.length > 0) {
    schema.sameAs = mergedConfig.sameAs;
  }

  // Add contact point if provided
  if (mergedConfig.contactPoint) {
    schema.contactPoint = mergedConfig.contactPoint;
  }

  // Add email if provided
  if (mergedConfig.email) {
    schema.email = mergedConfig.email;
  }

  // Add telephone if provided
  if (mergedConfig.telephone) {
    schema.telephone = mergedConfig.telephone;
  }

  // Add founding date if provided
  if (mergedConfig.foundingDate) {
    schema.foundingDate = mergedConfig.foundingDate;
  }

  return schema;
}

/**
 * Creates a minimal organization reference (for use within other schemas)
 */
export function createOrganizationRef(
  name: string = defaults.name,
  url?: string
): { '@type': 'Organization'; name: string; url?: string } {
  const ref: { '@type': 'Organization'; name: string; url?: string } = {
    '@type': 'Organization',
    name,
  };
  if (url) {
    ref.url = url;
  }
  return ref;
}

/**
 * Creates a publisher object with logo (commonly used in Article schemas)
 */
export function createPublisher(
  name: string = defaults.name,
  logoUrl: string = defaults.logo
): { '@type': 'Organization'; name: string; logo: ImageObject } {
  return {
    '@type': 'Organization',
    name,
    logo: {
      '@type': 'ImageObject',
      url: logoUrl,
    },
  };
}
