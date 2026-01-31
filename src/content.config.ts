/**
 * Content Collections Configuration
 * 
 * This file defines all content collections for the site.
 * See: https://docs.astro.build/en/guides/content-collections/
 */

import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Blog Collection Schema
 * 
 * Defines the structure and validation for blog posts.
 * All frontmatter properties are type-checked and validated at build time.
 * 
 * Image Guidelines:
 * - heroImage: Main featured image (1200x630px recommended for social sharing)
 * - Use relative paths for local images: ./images/my-image.jpg
 * - Images should be stored alongside the post or in src/assets/blog/
 */
const blog = defineCollection({
  // Load all markdown files from src/data/blog
  loader: glob({ pattern: '**/*.md', base: './src/data/blog' }),
  
  schema: z.object({
    // Required fields
    title: z.string().max(70, 'Title should be under 70 characters for SEO'),
    description: z.string().max(160, 'Description should be under 160 characters for SEO'),
    pubDate: z.coerce.date(),
    
    // Optional fields
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Monsoft Solutions'),
    
    // Hero Image (Vercel Blob URL)
    heroImage: z.string().url().optional(),
    heroImageAlt: z.string().optional(),
    
    // SEO & Social (ogImage falls back to heroImage if not set)
    ogImage: z.string().optional(),
    canonicalURL: z.string().url().optional(),
    
    // Categorization
    category: z.enum([
      'AI & Automation',
      'Web Development',
      'Business Growth',
      'Technology Trends',
      'Case Studies',
      'Guides & Tutorials',
      'Local Business',
      'Medical & Aesthetics'
    ]),
    tags: z.array(z.string()).default([]),
    
    // Content control
    draft: z.boolean().default(false),
    featured: z.boolean().default(false),
    
    // Reading experience
    readingTime: z.string().optional(), // e.g., "5 min read"
  }),
});

// Export all collections
export const collections = { blog };
