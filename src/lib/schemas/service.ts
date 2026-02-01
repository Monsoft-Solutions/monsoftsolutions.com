/**
 * Service Schema Builder
 * Creates schema.org Service structured data
 */

import type { ServiceSchema, Offer } from './types';
import { COMPANY } from './config';
import { createOrganizationRefFull } from './organization';

export interface ServiceConfig {
  name?: string;
  serviceType: string;
  description: string;
  url?: string;
  areaServed?: string | string[];
  provider?: {
    name: string;
    url?: string;
  };
  priceRange?: string;
  offers?: {
    availability?: 'InStock' | 'OnlineOnly' | 'LimitedAvailability';
    price?: number | string;
    priceCurrency?: string;
  };
  rating?: {
    value: number;
    reviewCount?: number;
    bestRating?: number;
  };
}

/**
 * Creates a Service schema
 */
export function createServiceSchema(config: ServiceConfig): ServiceSchema {
  const provider = config.provider ?? { name: COMPANY.name, url: COMPANY.url };

  const schema: ServiceSchema = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    serviceType: config.serviceType,
    description: config.description,
    provider: createOrganizationRefFull(provider.name, provider.url),
  };

  // Add name if provided
  if (config.name) {
    schema.name = config.name;
  }

  // Add area served
  if (config.areaServed) {
    schema.areaServed = config.areaServed;
  }

  // Add offers
  if (config.offers) {
    const offer: Offer = {
      '@type': 'Offer',
    };
    if (config.offers.availability) {
      offer.availability = `https://schema.org/${config.offers.availability}`;
    }
    if (config.offers.price !== undefined) {
      offer.price = config.offers.price;
      offer.priceCurrency = config.offers.priceCurrency || 'USD';
    }
    schema.offers = offer;
  }

  // Add rating
  if (config.rating) {
    schema.aggregateRating = {
      '@type': 'AggregateRating',
      ratingValue: config.rating.value,
      reviewCount: config.rating.reviewCount,
      bestRating: config.rating.bestRating || 5,
    };
  }

  return schema;
}

/**
 * Pre-configured service schemas for Monsoft Solutions services
 */
export const serviceSchemas = {
  automation: (): ServiceSchema =>
    createServiceSchema({
      name: 'Business Process Automation',
      serviceType: 'Business Process Automation',
      description:
        'Custom automation workflows that eliminate manual work, reduce errors, and scale your operations without adding headcount.',
      areaServed: 'Worldwide',
      offers: { availability: 'InStock' },
    }),

  aiAssistants: (): ServiceSchema =>
    createServiceSchema({
      name: 'AI Assistants & Chatbots',
      serviceType: 'AI Chatbot Development',
      description:
        'Custom AI assistants and chatbots that handle customer inquiries, qualify leads, and provide 24/7 support.',
      areaServed: 'Worldwide',
      offers: { availability: 'InStock' },
    }),

  development: (): ServiceSchema =>
    createServiceSchema({
      name: 'Custom Software Development',
      serviceType: 'Software Development',
      description:
        'Full-stack custom software development services including web applications, APIs, and enterprise solutions.',
      areaServed: 'Worldwide',
      offers: { availability: 'InStock' },
    }),

  aesthetics: (): ServiceSchema =>
    createServiceSchema({
      name: 'AI Solutions for Aesthetic Practices',
      serviceType: 'Healthcare Technology Services',
      description:
        'AI-powered software solutions tailored for plastic surgery clinics and aesthetic practices, including patient management and marketing automation.',
      areaServed: 'United States',
      offers: { availability: 'InStock' },
    }),

  localBusiness: (): ServiceSchema =>
    createServiceSchema({
      name: 'Local Business Digital Solutions',
      serviceType: 'Digital Marketing and Automation',
      description:
        'Comprehensive digital solutions for local businesses including AI automation, online presence optimization, and customer engagement tools.',
      areaServed: 'United States',
      offers: { availability: 'InStock' },
    }),

  seo: (): ServiceSchema =>
    createServiceSchema({
      name: 'SEO & Digital Marketing',
      serviceType: 'Search Engine Optimization',
      description:
        'Data-driven SEO and digital marketing services to improve online visibility and drive qualified traffic.',
      areaServed: 'Worldwide',
      offers: { availability: 'InStock' },
    }),

  websites: (): ServiceSchema =>
    createServiceSchema({
      name: 'Website Design & Development',
      serviceType: 'Web Design and Development',
      description:
        'High-performance, conversion-optimized websites built with modern technologies and best practices.',
      areaServed: 'Worldwide',
      offers: { availability: 'InStock' },
    }),
};
