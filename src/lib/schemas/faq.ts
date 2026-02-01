/**
 * FAQPage Schema Builder
 * Creates schema.org FAQPage structured data for FAQ sections
 */

import type { FAQPageSchema, FAQQuestion } from './types';

export interface FAQItem {
  question: string;
  answer: string;
}

/**
 * Creates an FAQPage schema from an array of question-answer pairs
 */
export function createFAQSchema(faqs: FAQItem[]): FAQPageSchema {
  const mainEntity: FAQQuestion[] = faqs.map((faq) => ({
    '@type': 'Question',
    name: faq.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: faq.answer,
    },
  }));

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity,
  };
}

/**
 * Creates an FAQPage schema from HTML content
 * Extracts h3 elements as questions and following p elements as answers
 * Useful for parsing FAQ sections from rendered content
 */
export function createFAQSchemaFromItems(
  items: Array<{ title: string; content: string }>
): FAQPageSchema {
  return createFAQSchema(
    items.map((item) => ({
      question: item.title,
      answer: item.content,
    }))
  );
}

/**
 * Helper to extract FAQ items from service page data structures
 */
export function extractFAQsFromServicePage(
  faqItems: Array<{ title?: string; question?: string; description?: string; answer?: string }>
): FAQItem[] {
  return faqItems.map((item) => ({
    question: item.title || item.question || '',
    answer: item.description || item.answer || '',
  }));
}
