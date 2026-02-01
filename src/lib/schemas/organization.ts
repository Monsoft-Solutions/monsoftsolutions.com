/**
 * Organization Schema Builder
 * Creates schema.org Organization structured data
 */

import type { OrganizationSchema, PostalAddress, ContactPoint, ImageObject } from './types';
import { COMPANY, SCHEMA_IDS } from './config';

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

/**
 * Creates an Organization schema with sensible defaults for Monsoft Solutions
 */
export function createOrganizationSchema(config: OrganizationConfig = {}): OrganizationSchema {
  const schema: OrganizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': SCHEMA_IDS.organization,
    name: config.name ?? COMPANY.name,
    url: config.url ?? COMPANY.url,
    logo: config.logo ?? COMPANY.logo,
    description: config.description ?? COMPANY.description,
  };

  // Add address
  const address = config.address ?? COMPANY.address;
  if (address) {
    schema.address = {
      '@type': 'PostalAddress',
      ...address,
    };
  }

  // Add social profiles
  const sameAs = config.sameAs ?? COMPANY.sameAs;
  if (sameAs && sameAs.length > 0) {
    schema.sameAs = [...sameAs];
  }

  // Add contact point if provided
  if (config.contactPoint) {
    schema.contactPoint = config.contactPoint;
  }

  // Add email if provided
  if (config.email) {
    schema.email = config.email;
  }

  // Add telephone if provided
  if (config.telephone) {
    schema.telephone = config.telephone;
  }

  // Add founding date if provided
  if (config.foundingDate) {
    schema.foundingDate = config.foundingDate;
  }

  return schema;
}

/**
 * Creates a minimal organization reference using @id (for linking within @graph)
 */
export function createOrganizationRef(): { '@id': string } {
  return { '@id': SCHEMA_IDS.organization };
}

/**
 * Creates a full organization reference (for use outside @graph context)
 */
export function createOrganizationRefFull(
  name: string = COMPANY.name,
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
  name: string = COMPANY.name,
  logoUrl: string = COMPANY.logo
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
