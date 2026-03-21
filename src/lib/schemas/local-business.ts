/**
 * LocalBusiness Schema Builder
 * Creates schema.org LocalBusiness structured data
 */

import type {
  LocalBusinessSchema,
  PostalAddress,
  GeoCoordinates,
  OpeningHoursSpecification,
  AggregateRating,
} from './types';
import { COMPANY, SCHEMA_IDS } from './config';

export interface LocalBusinessConfig {
  name?: string;
  url?: string;
  type?: 'LocalBusiness' | 'ProfessionalService' | 'ITService';
  description?: string;
  image?: string | string[];
  logo?: string;
  address?: Partial<PostalAddress>;
  geo?: GeoCoordinates;
  telephone?: string;
  email?: string;
  priceRange?: string;
  openingHours?: OpeningHoursSpecification[];
  sameAs?: string[];
  aggregateRating?: AggregateRating;
  areaServed?: string | string[];
}

/**
 * Creates a LocalBusiness schema with sensible defaults for Monsoft Solutions
 */
export function createLocalBusinessSchema(config: LocalBusinessConfig = {}): LocalBusinessSchema {
  const schema: LocalBusinessSchema = {
    '@context': 'https://schema.org',
    '@type': config.type ?? 'ProfessionalService',
    '@id': SCHEMA_IDS.localBusiness,
    name: config.name ?? COMPANY.name,
    url: config.url ?? COMPANY.url,
    description: config.description ?? COMPANY.description,
    logo: config.logo ?? COMPANY.logo,
    image: config.image ?? COMPANY.image,
    email: config.email ?? COMPANY.email,
  };

  // Add address
  const address = config.address ?? COMPANY.address;
  if (address) {
    schema.address = {
      '@type': 'PostalAddress',
      ...address,
    };
  }

  // Add geo coordinates if provided
  if (config.geo) {
    schema.geo = config.geo;
  }

  // Add telephone if provided
  if (config.telephone) {
    schema.telephone = config.telephone;
  }

  // Add price range if provided
  if (config.priceRange) {
    schema.priceRange = config.priceRange;
  }

  // Add opening hours if provided
  if (config.openingHours && config.openingHours.length > 0) {
    schema.openingHoursSpecification = config.openingHours;
  }

  // Add social profiles
  const sameAs = config.sameAs ?? COMPANY.sameAs;
  if (sameAs && sameAs.length > 0) {
    schema.sameAs = [...sameAs];
  }

  // Add aggregate rating if provided
  if (config.aggregateRating) {
    schema.aggregateRating = config.aggregateRating;
  }

  // Add area served
  const areaServed = config.areaServed ?? [...COMPANY.areaServed];
  if (areaServed) {
    schema.areaServed = Array.isArray(areaServed) ? areaServed : areaServed;
  }

  return schema;
}

/**
 * Creates standard business hours for weekdays
 */
export function createWeekdayHours(
  opens: string = '09:00',
  closes: string = '18:00'
): OpeningHoursSpecification {
  return {
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    opens,
    closes,
  };
}
