/**
 * JSON-LD Schema Types
 * TypeScript interfaces for structured data schemas following schema.org vocabulary
 */

// Base types
export interface SchemaContext {
  '@context': 'https://schema.org';
}

export interface SchemaType {
  '@type': string;
}

export interface SchemaBase extends SchemaContext, SchemaType {}

// Reusable entity types
export interface PostalAddress {
  '@type': 'PostalAddress';
  streetAddress?: string;
  addressLocality?: string;
  addressRegion?: string;
  postalCode?: string;
  addressCountry?: string;
}

export interface ImageObject {
  '@type': 'ImageObject';
  url: string;
  width?: number;
  height?: number;
}

export interface ContactPoint {
  '@type': 'ContactPoint';
  telephone?: string;
  contactType?: string;
  email?: string;
  availableLanguage?: string | string[];
}

export interface OpeningHoursSpecification {
  '@type': 'OpeningHoursSpecification';
  dayOfWeek: string | string[];
  opens?: string;
  closes?: string;
}

export interface GeoCoordinates {
  '@type': 'GeoCoordinates';
  latitude: number;
  longitude: number;
}

export interface MonetaryAmount {
  '@type': 'MonetaryAmount';
  currency: string;
  value: number;
}

export interface PriceSpecification {
  '@type': 'PriceSpecification';
  price?: number | string;
  priceCurrency?: string;
  minPrice?: number;
  maxPrice?: number;
}

export interface Offer {
  '@type': 'Offer';
  price?: number | string;
  priceCurrency?: string;
  availability?: string;
  priceValidUntil?: string;
  url?: string;
}

export interface AggregateRating {
  '@type': 'AggregateRating';
  ratingValue: number | string;
  reviewCount?: number;
  bestRating?: number;
  worstRating?: number;
}

// Main schema types
export interface OrganizationSchema extends SchemaBase {
  '@type': 'Organization';
  name: string;
  url: string;
  logo?: string | ImageObject;
  description?: string;
  foundingDate?: string;
  address?: PostalAddress;
  contactPoint?: ContactPoint | ContactPoint[];
  sameAs?: string[];
  email?: string;
  telephone?: string;
}

export interface LocalBusinessSchema extends SchemaBase {
  '@type': 'LocalBusiness' | 'ProfessionalService' | 'ITService';
  name: string;
  url: string;
  '@id'?: string;
  image?: string | string[];
  logo?: string | ImageObject;
  description?: string;
  address?: PostalAddress;
  geo?: GeoCoordinates;
  telephone?: string;
  email?: string;
  priceRange?: string;
  openingHoursSpecification?: OpeningHoursSpecification[];
  sameAs?: string[];
  aggregateRating?: AggregateRating;
  areaServed?: string | string[];
}

export interface WebSiteSchema extends SchemaBase {
  '@type': 'WebSite';
  name: string;
  url: string;
  description?: string;
  publisher?: OrganizationSchema | { '@type': 'Organization'; name: string };
  potentialAction?: SearchAction | SearchAction[];
}

export interface SearchAction {
  '@type': 'SearchAction';
  target:
    | string
    | {
        '@type': 'EntryPoint';
        urlTemplate: string;
      };
  'query-input'?: string;
}

export interface BreadcrumbItem {
  '@type': 'ListItem';
  position: number;
  name: string;
  item?: string;
}

export interface BreadcrumbListSchema extends SchemaBase {
  '@type': 'BreadcrumbList';
  itemListElement: BreadcrumbItem[];
}

export interface FAQQuestion {
  '@type': 'Question';
  name: string;
  acceptedAnswer: {
    '@type': 'Answer';
    text: string;
  };
}

export interface FAQPageSchema extends SchemaBase {
  '@type': 'FAQPage';
  mainEntity: FAQQuestion[];
}

export interface ServiceSchema extends SchemaBase {
  '@type': 'Service';
  name?: string;
  serviceType: string;
  description?: string;
  provider?: OrganizationSchema | { '@type': 'Organization'; name: string; url?: string };
  areaServed?: string | string[];
  hasOfferCatalog?: OfferCatalog;
  offers?: Offer;
  aggregateRating?: AggregateRating;
}

export interface OfferCatalog {
  '@type': 'OfferCatalog';
  name: string;
  itemListElement?: (Offer | ServiceSchema)[];
}

export interface ProductSchema extends SchemaBase {
  '@type': 'Product' | 'SoftwareApplication';
  name: string;
  description?: string;
  image?: string | string[];
  brand?: { '@type': 'Brand'; name: string } | { '@type': 'Organization'; name: string };
  offers?: Offer | Offer[];
  aggregateRating?: AggregateRating;
  applicationCategory?: string;
  operatingSystem?: string;
  url?: string;
}

export interface SoftwareApplicationSchema extends SchemaBase {
  '@type': 'SoftwareApplication';
  name: string;
  description?: string;
  applicationCategory: string;
  operatingSystem?: string;
  offers?: Offer;
  aggregateRating?: AggregateRating;
  author?: OrganizationSchema | { '@type': 'Organization'; name: string };
  url?: string;
}

export interface ArticleSchema extends SchemaBase {
  '@type': 'Article' | 'BlogPosting' | 'TechArticle';
  headline: string;
  description?: string;
  image?: string | string[] | ImageObject;
  author?: PersonSchema | OrganizationSchema | { '@type': 'Person' | 'Organization'; name: string };
  publisher?: OrganizationSchema | { '@type': 'Organization'; name: string; logo?: ImageObject };
  datePublished: string;
  dateModified?: string;
  mainEntityOfPage?: { '@type': 'WebPage'; '@id': string };
  wordCount?: number;
  articleSection?: string;
  keywords?: string | string[];
}

export interface PersonSchema extends SchemaBase {
  '@type': 'Person';
  name: string;
  url?: string;
  image?: string | ImageObject;
  jobTitle?: string;
  worksFor?: OrganizationSchema | { '@type': 'Organization'; name: string };
}

export interface WebPageSchema extends SchemaBase {
  '@type': 'WebPage' | 'AboutPage' | 'ContactPage' | 'CollectionPage';
  name: string;
  description?: string;
  url?: string;
  isPartOf?: { '@type': 'WebSite'; name: string; url: string };
  breadcrumb?: BreadcrumbListSchema;
  mainEntity?: SchemaBase | SchemaBase[];
}

// Helper type for combining multiple schemas
export type CombinedSchema = SchemaBase[];
