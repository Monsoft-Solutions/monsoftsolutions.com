/**
 * BreadcrumbList Schema Builder
 * Creates schema.org BreadcrumbList structured data for navigation hierarchy
 */

import type { BreadcrumbListSchema, BreadcrumbItem } from './types';
import { BASE_URL } from './config';

export interface BreadcrumbConfig {
  items: {
    name: string;
    url?: string;
  }[];
  baseUrl?: string;
}

/**
 * Creates a BreadcrumbList schema from an array of breadcrumb items
 * The last item should not have a URL (it's the current page)
 */
export function createBreadcrumbSchema(config: BreadcrumbConfig): BreadcrumbListSchema {
  const { items, baseUrl = BASE_URL } = config;

  const itemListElement: BreadcrumbItem[] = items.map((item, index) => {
    const isLast = index === items.length - 1;
    const breadcrumbItem: BreadcrumbItem = {
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
    };

    // Only add item URL if not the last item (current page doesn't need URL)
    if (!isLast && item.url) {
      // Handle relative and absolute URLs
      breadcrumbItem.item = item.url.startsWith('http') ? item.url : `${baseUrl}${item.url}`;
    }

    return breadcrumbItem;
  });

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement,
  };
}

/**
 * Helper to create common breadcrumb paths
 */
export const breadcrumbPaths = {
  /**
   * Home > [Page Name]
   */
  simple: (pageName: string): BreadcrumbConfig => ({
    items: [{ name: 'Home', url: '/' }, { name: pageName }],
  }),

  /**
   * Home > Services > [Service Name]
   */
  service: (serviceName: string): BreadcrumbConfig => ({
    items: [
      { name: 'Home', url: '/' },
      { name: 'Services', url: '/services' },
      { name: serviceName },
    ],
  }),

  /**
   * Home > Products > [Product Name]
   */
  product: (productName: string): BreadcrumbConfig => ({
    items: [
      { name: 'Home', url: '/' },
      { name: 'Products', url: '/products' },
      { name: productName },
    ],
  }),

  /**
   * Home > Blog > [Post Title]
   */
  blogPost: (postTitle: string): BreadcrumbConfig => ({
    items: [{ name: 'Home', url: '/' }, { name: 'Blog', url: '/blog' }, { name: postTitle }],
  }),

  /**
   * Home > Blog > Category > [Category Name]
   */
  blogCategory: (categoryName: string): BreadcrumbConfig => ({
    items: [{ name: 'Home', url: '/' }, { name: 'Blog', url: '/blog' }, { name: categoryName }],
  }),

  /**
   * Home > Industries > [Industry Name]
   */
  industry: (industryName: string): BreadcrumbConfig => ({
    items: [
      { name: 'Home', url: '/' },
      { name: 'Industries', url: '/industries' },
      { name: industryName },
    ],
  }),
};

/**
 * Creates breadcrumbs from a URL path
 * Automatically generates breadcrumbs based on path segments
 */
export function createBreadcrumbsFromPath(
  pathname: string,
  currentPageName: string,
  baseUrl: string = BASE_URL
): BreadcrumbListSchema {
  // Remove leading/trailing slashes and split
  const segments = pathname
    .replace(/^\/|\/$/g, '')
    .split('/')
    .filter(Boolean);

  const items: { name: string; url?: string }[] = [{ name: 'Home', url: '/' }];

  // Build path incrementally
  let currentPath = '';
  segments.forEach((segment, index) => {
    currentPath += `/${segment}`;
    const isLast = index === segments.length - 1;

    // Format segment name (capitalize, replace hyphens)
    const name = isLast
      ? currentPageName
      : segment
          .split('-')
          .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');

    items.push({
      name,
      url: isLast ? undefined : currentPath,
    });
  });

  return createBreadcrumbSchema({ items, baseUrl });
}
