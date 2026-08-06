/**
 * JSON-LD Schema Library
 * Centralized schema builders for structured data across the site
 *
 * @example
 * import { createOrganizationSchema, createBreadcrumbSchema } from '@/lib/schemas';
 *
 * const schema = createOrganizationSchema();
 * const breadcrumbs = createBreadcrumbSchema({
 *   items: [
 *     { name: 'Home', url: '/' },
 *     { name: 'About' }
 *   ]
 * });
 */

// Config - single source of truth for company data
export { COMPANY, SCHEMA_IDS, BASE_URL } from './config';

// Types
export type {
  SchemaBase,
  SchemaRef,
  OrganizationSchema,
  LocalBusinessSchema,
  WebSiteSchema,
  BreadcrumbListSchema,
  FAQPageSchema,
  ServiceSchema,
  ProductSchema,
  SoftwareApplicationSchema,
  ArticleSchema,
  WebPageSchema,
  PersonSchema,
  PostalAddress,
  ImageObject,
  ContactPoint,
  Offer,
  AggregateRating,
  FAQQuestion,
  BreadcrumbItem,
  CombinedSchema,
} from './types';

// Organization
export {
  createOrganizationSchema,
  createOrganizationRef,
  createOrganizationRefFull,
  createPublisher,
  type OrganizationConfig,
} from './organization';

// Local Business
export {
  createLocalBusinessSchema,
  createWeekdayHours,
  type LocalBusinessConfig,
} from './local-business';

// Website
export {
  createWebSiteSchema,
  createSearchAction,
  createWebSiteWithBlogSearch,
  type WebSiteConfig,
} from './website';

// Breadcrumbs
export {
  createBreadcrumbSchema,
  createBreadcrumbsFromPath,
  breadcrumbPaths,
  type BreadcrumbConfig,
} from './breadcrumb';

// FAQ
export {
  createFAQSchema,
  createFAQSchemaFromItems,
  extractFAQsFromServicePage,
  type FAQItem,
} from './faq';

// Products
export {
  createProductSchema,
  createSoftwareApplicationSchema,
  createProductCollectionSchema,
  type ProductConfig,
  type SoftwareConfig,
} from './product';

// Services
export { createServiceSchema, serviceSchemas, type ServiceConfig } from './service';

// Articles
export {
  createArticleSchema,
  createBlogPostingSchema,
  createTechArticleSchema,
  estimateWordCount,
  extractKeywords,
  type ArticleConfig,
} from './article';

/**
 * Combines multiple schemas into an array for injection
 * Useful when a page needs multiple schema types
 */
export function combineSchemas(...schemas: object[]): object[] {
  return schemas;
}

/**
 * Wraps multiple schemas in a @graph structure
 * This is the recommended way to include multiple schemas on one page
 */
export function createSchemaGraph(...schemas: object[]): {
  '@context': 'https://schema.org';
  '@graph': object[];
} {
  // Remove @context from individual schemas to avoid duplication
  const cleanedSchemas = schemas.map((schema) => {
    const { '@context': _, ...rest } = schema as { '@context'?: string };
    return rest;
  });

  return {
    '@context': 'https://schema.org',
    '@graph': cleanedSchemas,
  };
}
