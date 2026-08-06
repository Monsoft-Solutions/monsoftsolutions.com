/**
 * Product & SoftwareApplication Schema Builder
 * Creates schema.org Product/SoftwareApplication structured data
 */

import type { ProductSchema, SoftwareApplicationSchema, Offer } from './types';
import { COMPANY } from './config';
import { createOrganizationRefFull } from './organization';

export interface ProductConfig {
  name: string;
  description: string;
  url?: string;
  image?: string | string[];
  brandName?: string;
  price?: number | string;
  priceCurrency?: string;
  availability?: 'InStock' | 'OutOfStock' | 'PreOrder' | 'SoldOut';
  rating?: {
    value: number;
    reviewCount?: number;
    bestRating?: number;
  };
}

export interface SoftwareConfig extends ProductConfig {
  applicationCategory:
    | 'BusinessApplication'
    | 'SocialNetworkingApplication'
    | 'HealthApplication'
    | 'CommunicationApplication'
    | 'DeveloperApplication'
    | 'FinanceApplication'
    | string;
  operatingSystem?: string;
  offers?: {
    price?: number | string;
    priceCurrency?: string;
    priceSpecification?: 'Free' | 'Freemium' | 'Subscription' | 'OneTime';
  };
}

/**
 * Creates a Product schema
 */
export function createProductSchema(config: ProductConfig): ProductSchema {
  const schema: ProductSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: config.name,
    description: config.description,
  };

  // Add URL
  if (config.url) {
    schema.url = config.url;
  }

  // Add image(s)
  if (config.image) {
    schema.image = config.image;
  }

  // Add brand
  if (config.brandName) {
    schema.brand = {
      '@type': 'Brand',
      name: config.brandName,
    };
  }

  // Add offer/pricing
  if (config.price !== undefined || config.availability) {
    const offer: Offer = {
      '@type': 'Offer',
    };
    if (config.price !== undefined) {
      offer.price = config.price;
      offer.priceCurrency = config.priceCurrency || 'USD';
    }
    if (config.availability) {
      offer.availability = `https://schema.org/${config.availability}`;
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
 * Creates a SoftwareApplication schema (better for SaaS products)
 */
export function createSoftwareApplicationSchema(config: SoftwareConfig): SoftwareApplicationSchema {
  const schema: SoftwareApplicationSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: config.name,
    description: config.description,
    applicationCategory: config.applicationCategory,
    author: createOrganizationRefFull(COMPANY.name, COMPANY.url),
  };

  // Add URL
  if (config.url) {
    schema.url = config.url;
  }

  // Add operating system
  if (config.operatingSystem) {
    schema.operatingSystem = config.operatingSystem;
  }

  // Add offers
  if (config.offers) {
    schema.offers = {
      '@type': 'Offer',
      price: config.offers.price ?? 0,
      priceCurrency: config.offers.priceCurrency || 'USD',
    };
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
 * Creates a collection of software products (for products page)
 */
export function createProductCollectionSchema(
  products: SoftwareConfig[]
): SoftwareApplicationSchema[] {
  return products.map((product) => createSoftwareApplicationSchema(product));
}
