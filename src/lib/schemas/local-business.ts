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

// Default local business data for Monsoft Solutions
const defaults: Required<
  Pick<
    LocalBusinessConfig,
    'name' | 'url' | 'type' | 'description' | 'logo' | 'address' | 'sameAs' | 'email' | 'areaServed'
  >
> = {
  name: 'Monsoft Solutions',
  url: 'https://monsoftsolutions.com',
  type: 'ProfessionalService',
  description:
    'AI-first software company specializing in business automation, custom software development, and AI solutions for plastic surgery clinics and local businesses.',
  logo: 'https://monsoftsolutions.com/logo.svg',
  email: 'hello@monsoftsolutions.com',
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
};

/**
 * Creates a LocalBusiness schema with sensible defaults for Monsoft Solutions
 */
export function createLocalBusinessSchema(config: LocalBusinessConfig = {}): LocalBusinessSchema {
  const mergedConfig = { ...defaults, ...config };

  const schema: LocalBusinessSchema = {
    '@context': 'https://schema.org',
    '@type': mergedConfig.type,
    '@id': `${mergedConfig.url}/#localbusiness`,
    name: mergedConfig.name,
    url: mergedConfig.url,
    description: mergedConfig.description,
  };

  // Add logo
  if (mergedConfig.logo) {
    schema.logo = mergedConfig.logo;
  }

  // Add image(s)
  if (mergedConfig.image) {
    schema.image = mergedConfig.image;
  }

  // Add address
  if (mergedConfig.address) {
    schema.address = {
      '@type': 'PostalAddress',
      ...mergedConfig.address,
    };
  }

  // Add geo coordinates
  if (mergedConfig.geo) {
    schema.geo = mergedConfig.geo;
  }

  // Add contact info
  if (mergedConfig.telephone) {
    schema.telephone = mergedConfig.telephone;
  }

  if (mergedConfig.email) {
    schema.email = mergedConfig.email;
  }

  // Add price range
  if (mergedConfig.priceRange) {
    schema.priceRange = mergedConfig.priceRange;
  }

  // Add opening hours
  if (mergedConfig.openingHours && mergedConfig.openingHours.length > 0) {
    schema.openingHoursSpecification = mergedConfig.openingHours;
  }

  // Add social profiles
  if (mergedConfig.sameAs && mergedConfig.sameAs.length > 0) {
    schema.sameAs = mergedConfig.sameAs;
  }

  // Add aggregate rating
  if (mergedConfig.aggregateRating) {
    schema.aggregateRating = mergedConfig.aggregateRating;
  }

  // Add area served
  if (mergedConfig.areaServed) {
    schema.areaServed = mergedConfig.areaServed;
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
