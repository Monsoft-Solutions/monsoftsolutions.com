# Blog System Documentation

This document explains how the blog works in the Monsoft Solutions website.

## Overview

The blog uses **Astro Content Collections** to manage blog posts as Markdown files. This provides:

- Type-safe frontmatter with Zod validation
- Automatic TypeScript types
- Optimized build-time rendering
- Easy content management without a CMS

## File Structure

```
src/
├── content.config.ts          # Collection definitions & schemas
├── data/
│   └── blog/                  # Blog post markdown files
│       ├── post-1.md
│       └── post-2.md
├── layouts/
│   └── BlogPost.astro         # Individual post layout
└── pages/
    └── blog/
        ├── index.astro        # Blog listing page
        └── [...slug].astro    # Dynamic post pages
```

## Creating a New Blog Post

### 1. Create a Markdown File

Create a new `.md` file in `src/data/blog/`. The filename becomes the URL slug:

```
src/data/blog/my-new-post.md → /blog/my-new-post
```

### 2. Add Frontmatter

Every post requires frontmatter with these fields:

```yaml
---
title: "Your Post Title"                    # Required, max 70 chars for SEO
description: "A brief description"           # Required, max 160 chars for SEO
pubDate: 2026-01-31                          # Required, YYYY-MM-DD format
author: "Monsoft Solutions"                  # Optional, defaults to "Monsoft Solutions"
category: "AI & Automation"                  # Required, must match allowed categories
tags: ["AI", "Automation"]                   # Optional, array of strings
featured: false                              # Optional, shows in featured section
draft: false                                 # Optional, true hides from production
readingTime: "5 min read"                    # Optional, displayed on post
updatedDate: 2026-02-01                      # Optional, for updated posts
ogImage: "/images/my-post-og.jpg"            # Optional, Open Graph image
---
```

### Allowed Categories

Posts must use one of these categories:
- `AI & Automation`
- `Web Development`
- `Business Growth`
- `Technology Trends`
- `Case Studies`
- `Guides & Tutorials`

### 3. Write Content

Write your content in Markdown below the frontmatter:

```markdown
---
title: "My Post Title"
# ... other frontmatter
---

Your introduction paragraph here.

## First Section

Content for first section...

### Subsection

More details...
```

## Features

### Featured Posts

Set `featured: true` in frontmatter to display a post prominently at the top of the blog page.

### Draft Mode

Set `draft: true` to hide a post from production builds. Drafts are excluded from:
- Blog listing page
- Sitemap
- RSS feed (if added)

### Tags

Tags create linkable hashtags on each post. Use consistent naming:
- Capitalize properly: "AI" not "ai"
- Use spaces for multi-word: "Small Business" not "small-business"

### Categories

Categories group related posts. Each post must have exactly one category.

## SEO Optimization

Each post automatically generates:

- Meta title and description
- Open Graph tags for social sharing
- Twitter Card tags
- Article structured data (JSON-LD)
- Canonical URLs

**Best Practices:**
- Keep titles under 70 characters
- Keep descriptions under 160 characters
- Use descriptive, keyword-rich filenames
- Include relevant internal links

## Styling

Blog posts inherit global styles plus custom markdown styling from `BlogPost.astro`:

- Typography optimized for reading
- Code blocks with syntax highlighting
- Responsive images
- Blockquote styling
- List formatting

## Querying Posts

In any Astro component, you can query posts:

```typescript
import { getCollection } from 'astro:content';

// Get all published posts
const posts = await getCollection('blog', ({ data }) => !data.draft);

// Sort by date (newest first)
const sortedPosts = posts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);

// Filter by category
const aiPosts = posts.filter(p => p.data.category === 'AI & Automation');

// Get featured posts
const featuredPosts = posts.filter(p => p.data.featured);
```

## Rendering Posts

To render a post's content:

```typescript
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'my-post-slug');
const { Content, headings } = await render(post);
```

Then in your template:

```astro
<Content />
```

## Adding New Features

### Adding a Category

1. Update the category enum in `src/content.config.ts`:

```typescript
category: z.enum([
  'AI & Automation',
  'Web Development',
  // Add new category here
  'New Category',
]),
```

2. Optionally add category-specific pages in `src/pages/blog/category/`

### Adding Fields

1. Add the field to the schema in `src/content.config.ts`
2. Update `BlogPost.astro` to use the new field
3. Update this documentation

## Common Issues

### Build Errors

**"Invalid frontmatter"**: Check that all required fields are present and categories match the allowed list.

**"Cannot find module"**: Run `npm install` and restart the dev server.

### Posts Not Showing

1. Check `draft` isn't set to `true`
2. Verify the file is in `src/data/blog/`
3. Confirm frontmatter syntax is valid YAML

## Resources

- [Astro Content Collections Docs](https://docs.astro.build/en/guides/content-collections/)
- [Astro Markdown Guide](https://docs.astro.build/en/guides/markdown-content/)
- [Zod Schema Reference](https://zod.dev/)
