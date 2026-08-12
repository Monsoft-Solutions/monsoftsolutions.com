/**
 * WebSite Schema Builder
 * Creates schema.org WebSite structured data with optional SearchAction
 */

import type { WebSiteSchema, SearchAction } from './types';
import { COMPANY, SCHEMA_IDS } from './config';
import { createOrganizationRef } from './organization';

export interface WebSiteConfig {
  name?: string;
  url?: string;
  description?: string;
  /**
   * Enable SearchAction for sitelinks search box in Google
   * Set to false to disable, or provide custom config
   */
  searchAction?:
    | boolean
    | {
        urlTemplate: string;
        queryInput?: string;
      };
}

/**
 * Creates a WebSite schema with optional SearchAction
 * SearchAction is enabled by default (points to /blog search)
 */
export function createWebSiteSchema(config: WebSiteConfig = {}): WebSiteSchema {
  const url = config.url ?? COMPANY.url;

  const schema: WebSiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': SCHEMA_IDS.website,
    name: config.name ?? COMPANY.name,
    url: url,
    description: config.description ?? COMPANY.description,
    publisher: createOrganizationRef(),
  };

  // Add search action (enabled by default)
  const searchAction = config.searchAction ?? true;
  if (searchAction !== false) {
    if (searchAction === true) {
      // Default search action pointing to blog
      schema.potentialAction = createSearchAction(`${url}/blog?q={search_term_string}`);
    } else {
      // Custom search action
      schema.potentialAction = createSearchAction(
        searchAction.urlTemplate,
        searchAction.queryInput
      );
    }
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
 * @deprecated Use createWebSiteSchema() which now includes search by default
 */
export function createWebSiteWithBlogSearch(baseUrl: string = COMPANY.url): WebSiteSchema {
  return createWebSiteSchema({
    url: baseUrl,
    searchAction: {
      urlTemplate: `${baseUrl}/blog?q={search_term_string}`,
    },
  });
}
