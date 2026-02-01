/**
 * WebSite Schema Builder
 * Creates schema.org WebSite structured data with optional SearchAction
 */

import type { WebSiteSchema, SearchAction } from './types';
import { createOrganizationRef } from './organization';

export interface WebSiteConfig {
  name?: string;
  url?: string;
  description?: string;
  publisher?: { name: string; url?: string };
  searchAction?: {
    urlTemplate: string;
    queryInput?: string;
  };
}

// Default website data for Monsoft Solutions
const defaults: Required<Pick<WebSiteConfig, 'name' | 'url' | 'description'>> = {
  name: 'Monsoft Solutions',
  url: 'https://monsoftsolutions.com',
  description:
    'AI-first software company building intelligent solutions for plastic surgery clinics and local businesses. Custom development, business automation, and AI-powered products.',
};

/**
 * Creates a WebSite schema with optional SearchAction
 */
export function createWebSiteSchema(config: WebSiteConfig = {}): WebSiteSchema {
  const mergedConfig = { ...defaults, ...config };

  const schema: WebSiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: mergedConfig.name,
    url: mergedConfig.url,
    description: mergedConfig.description,
    publisher: createOrganizationRef(
      mergedConfig.publisher?.name || defaults.name,
      mergedConfig.publisher?.url || defaults.url
    ),
  };

  // Add search action if provided
  if (mergedConfig.searchAction) {
    schema.potentialAction = createSearchAction(
      mergedConfig.searchAction.urlTemplate,
      mergedConfig.searchAction.queryInput
    );
  }

  return schema;
}

/**
 * Creates a SearchAction for the WebSite schema
 * This enables sitelinks search box in Google search results
 */
export function createSearchAction(
  urlTemplate: string,
  queryInput: string = 'required name=search_term_string'
): SearchAction {
  return {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: urlTemplate,
    },
    'query-input': queryInput,
  };
}

/**
 * Creates a WebSite schema with blog search capability
 */
export function createWebSiteWithBlogSearch(
  baseUrl: string = 'https://monsoftsolutions.com'
): WebSiteSchema {
  return createWebSiteSchema({
    url: baseUrl,
    searchAction: {
      urlTemplate: `${baseUrl}/blog?q={search_term_string}`,
      queryInput: 'required name=search_term_string',
    },
  });
}
