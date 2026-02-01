/**
 * Article Schema Builder
 * Creates schema.org Article/BlogPosting structured data
 */

import type { ArticleSchema } from './types';
import { COMPANY } from './config';
import { createPublisher } from './organization';

export interface ArticleConfig {
  headline: string;
  description: string;
  url: string;
  datePublished: Date | string;
  dateModified?: Date | string;
  authorName?: string;
  authorType?: 'Person' | 'Organization';
  image?: string | string[];
  wordCount?: number;
  articleSection?: string;
  keywords?: string[];
  publisherName?: string;
  publisherLogo?: string;
}

/**
 * Formats a date to ISO string format
 */
function formatDate(date: Date | string): string {
  if (typeof date === 'string') {
    return new Date(date).toISOString();
  }
  return date.toISOString();
}

/**
 * Creates an Article schema (for blog posts, guides, etc.)
 */
export function createArticleSchema(config: ArticleConfig): ArticleSchema {
  const schema: ArticleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: config.headline,
    description: config.description,
    datePublished: formatDate(config.datePublished),
    dateModified: formatDate(config.dateModified || config.datePublished),
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': config.url,
    },
  };

  // Add author
  const authorType = config.authorType || 'Organization';
  schema.author = {
    '@type': authorType,
    name: config.authorName || COMPANY.name,
  };

  // Add publisher
  schema.publisher = createPublisher(
    config.publisherName || COMPANY.name,
    config.publisherLogo || COMPANY.logo
  );

  // Add image
  if (config.image) {
    schema.image = config.image;
  }

  // Add word count
  if (config.wordCount) {
    schema.wordCount = config.wordCount;
  }

  // Add article section (category)
  if (config.articleSection) {
    schema.articleSection = config.articleSection;
  }

  // Add keywords
  if (config.keywords && config.keywords.length > 0) {
    schema.keywords = config.keywords;
  }

  return schema;
}

/**
 * Creates a BlogPosting schema (more specific than Article)
 */
export function createBlogPostingSchema(
  config: ArticleConfig
): ArticleSchema & { '@type': 'BlogPosting' } {
  const article = createArticleSchema(config);
  return {
    ...article,
    '@type': 'BlogPosting',
  };
}

/**
 * Creates a TechArticle schema (for technical guides)
 */
export function createTechArticleSchema(
  config: ArticleConfig
): ArticleSchema & { '@type': 'TechArticle' } {
  const article = createArticleSchema(config);
  return {
    ...article,
    '@type': 'TechArticle',
  };
}

/**
 * Estimates word count from text content
 */
export function estimateWordCount(text: string): number {
  return text.split(/\s+/).filter((word) => word.length > 0).length;
}

/**
 * Extracts keywords from tags array (filters and formats for SEO)
 */
export function extractKeywords(tags: string[]): string[] {
  return tags.map((tag) => tag.toLowerCase().trim()).filter((tag) => tag.length > 2);
}
